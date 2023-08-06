"""
TODO:
    * Implement histograms
"""
import logging
import numbers

import datasketches
import pandas as pd

from whylogs.proto import (
    NumbersMessage,
    NumberSummary,
    TrackerMessage,
    TrackerSummary,
    UniqueCountSummary,
)
from whylogs.util import dsketch, stats
from whylogs.v2.core.statistics.datatypes import (
    FloatTracker,
    IntTracker,
    VarianceTracker,
)
from whylogs.v2.core.statistics.thetasketch import ThetaSketch
from whylogs.v2.core.summaryconverters import (
    histogram_from_sketch,
    quantiles_from_sketch,
)
from whylogs.v2.core.tracker import Tracker

# Parameter controlling histogram accuracy.  Larger = more accurate
DEFAULT_HIST_K = 256
_NUMBER_TRACKER_TYPE = 5
logger = logging.getLogger(__name__)


class NumberTracker(Tracker):
    """
    Class to track statistics for numeric data.

    Parameters
    ----------
    variance
        Tracker to follow the variance
    floats
        Float tracker for tracking all floats
    ints
        Integer tracker

    Attributes
    ----------
    variance
        See above
    floats
        See above
    ints
        See above
    theta_sketch : `whylogs.logs.core.statistics.thetasketch.ThetaSketch`
        Sketch which tracks approximate cardinality
    """

    def __init__(
        self,
        variance: VarianceTracker = None,
        floats: FloatTracker = None,
        ints: IntTracker = None,
        theta_sketch: ThetaSketch = None,
        histogram: datasketches.kll_floats_sketch = None,
    ):
        # Our own trackers
        if variance is None:
            variance = VarianceTracker()
        if floats is None:
            floats = FloatTracker()
        if ints is None:
            ints = IntTracker()
        if theta_sketch is None:
            theta_sketch = ThetaSketch()
        if histogram is None:
            histogram = datasketches.kll_floats_sketch(DEFAULT_HIST_K)
        self.variance = variance
        self.floats = floats
        self.ints = ints
        self.theta_sketch = theta_sketch
        self.histogram = histogram
        self.name = "NumberTracker"

    @property
    def count(self):
        return self.variance.count

    def has_unique_count(self) -> bool:
        return True

    def get_unique_count_summary(self) -> UniqueCountSummary:
        self.theta_sketch.to_summary()

    def track(self, number, data_type=None):
        """
        Add a number to statistics tracking

        Parameters
        ----------
        number : int, float
            A numeric value
        """
        # TODO: simplify with data_type passed in
        if pd.isnull(number) or (not isinstance(number, numbers.Real)) or isinstance(number, bool):
            # XXX: this type checking may still be fragile in python.
            return
        self.variance.update(number)
        # self.theta_sketch.update(number)
        # TODO: histogram update
        # Update floats/ints counting
        f_value = float(number)
        self.theta_sketch.update(f_value)
        self.histogram.update(f_value)
        if self.floats.count > 0:
            self.floats.update(f_value)
        # Note: this type checking is fragile in python.  May want to include
        # numpy.integer in the type check
        elif isinstance(number, int):
            self.ints.update(number)
        else:
            self.floats.add_integers(self.ints)
            self.ints.set_defaults()
            self.floats.update(f_value)

    def merge(self, other):
        # Make a copy of the histogram
        hist_copy = datasketches.kll_floats_sketch.deserialize(self.histogram.serialize())
        hist_copy.merge(other.histogram)

        theta_sketch = self.theta_sketch.merge(other.theta_sketch)
        return NumberTracker(
            variance=self.variance.merge(other.variance),
            floats=self.floats.merge(other.floats),
            ints=self.ints.merge(other.ints),
            theta_sketch=theta_sketch,
            histogram=hist_copy,
        )

    def to_protobuf(self):
        """
        Return the object serialized as a protobuf message
        """
        opts = dict(
            variance=self.variance.to_protobuf(),
            compact_theta=self.theta_sketch.serialize(),
            histogram=self.histogram.serialize(),
        )
        if self.floats.count > 0:
            opts["doubles"] = self.floats.to_protobuf()
        elif self.ints.count > 0:
            opts["longs"] = self.ints.to_protobuf()
        msg = NumbersMessage(**opts)

        return TrackerMessage(
            name=self.name,
            type_index=_NUMBER_TRACKER_TYPE,
            numbers=msg,
        )

    @staticmethod
    def from_protobuf(message: TrackerMessage) -> "NumberTracker":
        """
        Load from a protobuf message

        Returns
        -------
        number_tracker : NumberTracker
        """
        if not hasattr(message, "type_index"):
            raise ValueError(f"Attempting to deserialize a message to NumberTracker without type_index {message}")
        if message.type_index != _NUMBER_TRACKER_TYPE:
            raise ValueError(f"Attempting to deserialize a message to NumberTracker with type_index not {_NUMBER_TRACKER_TYPE}->{message}")
        if not message.numbers:
            logger.warning(f"Possible missing data, deserialized an empty NumberTracker message {message}")
            return NumberTracker()
        theta = None
        if message.numbers.compact_theta is not None and len(message.numbers.compact_theta) > 0:
            theta = ThetaSketch.deserialize(message.numbers.compact_theta)
        elif message.numbers.theta is not None and len(message.numbers.theta) > 0:
            logger.warning("Possible missing data. Non-compact theta sketches are no longer supported")

        opts = dict(
            theta_sketch=theta,
            variance=VarianceTracker.from_protobuf(message.numbers.variance),
            histogram=dsketch.deserialize_kll_floats_sketch(message.numbers.histogram),
        )
        if message.numbers.HasField("doubles"):
            opts["floats"] = FloatTracker.from_protobuf(message.numbers.doubles)
        if message.numbers.HasField("longs"):
            opts["ints"] = IntTracker.from_protobuf(message.numbers.longs)
        return NumberTracker(**opts)

    def to_summary(self) -> TrackerSummary:
        """
        Construct a `NumberSummary` message

        Returns
        -------
        summary : NumberSummary
            Summary of the tracker statistics
        """
        if self.variance.count == 0:
            return

        stddev = self.variance.stddev()
        doubles = self.floats.to_protobuf()
        if doubles.count > 0:
            mean = self.floats.mean()
            min = doubles.min
            max = doubles.max
        else:
            mean = self.ints.mean()
            min = float(self.ints.min)
            max = float(self.ints.max)

        unique_count = self.theta_sketch.to_summary()
        histogram = histogram_from_sketch(self.histogram)
        quant = quantiles_from_sketch(self.histogram)
        num_records = self.variance.count
        cardinality = unique_count.estimate
        if doubles.count > 0:
            discrete = False
        else:
            discrete = stats.is_discrete(num_records, cardinality)

        return TrackerSummary(
            name=self.name,
            type_index=_NUMBER_TRACKER_TYPE,
            numbers=NumberSummary(
                count=self.variance.count,
                stddev=stddev,
                min=min,
                max=max,
                mean=mean,
                histogram=histogram,
                quantiles=quant,
                unique_count=unique_count,
                is_discrete=discrete,
            ),
        )
