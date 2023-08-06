from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, List, Union, cast

import numpy as np

from ..utils import VectorizedFunction
from .aliases import NumericValue, Value
from .functions import FuzzyNumber, Interval, VectorizedFuzzyNumber


def numeric_value(
    value: Union[NumericValue, FuzzyNumber, VectorizedFuzzyNumber]
) -> NumericValue:
    """Convert value to numeric.

    Used to keep numeric values as is, and convert
    :class:`functions.FuzzyNumber` to numerical value.

    :param value:
    :return:
    """
    return (
        value.average()
        if isinstance(value, FuzzyNumber)
        or isinstance(value, VectorizedFuzzyNumber)
        else value
    )


class PreferenceDirection(Enum):
    """Enumeration of MCDA preference directions."""

    MIN = auto()
    MAX = auto()

    @classmethod
    def has_value(cls, x: "PreferenceDirection") -> bool:
        """Check if value is in enumeration.

        :param x:
        :return:
        """
        return x in cls

    @classmethod
    def content_message(cls) -> str:
        """Return list of items and their values.

        :return:
        """
        s = ", ".join(f"{item}: {item.value}" for item in cls)
        return "PreferenceDirection only has following values " + s


class Scale(ABC):
    """Basic abstract class for MCDA scale."""

    @abstractmethod
    def __contains__(self, x: Value) -> bool:  # pragma: nocover
        """Check if values are inside scale.

        :param x:
        :return:
        """
        pass


class NominativeScale(Scale):
    """This class implements a MCDA nominative scale.

    :param labels:
    """

    def __init__(self, labels: List[Value]):
        """Constructor method"""
        Scale.__init__(self)
        self.labels = labels

    def __contains__(self, x: Value) -> bool:
        """Check if values are inside scale.

        :param x:
        :return:
        """
        return x in self.labels


class QuantitativeScale(Scale, Interval):
    """Class for quantitative scale.

    :param dmin: min boundary of scale
    :param dmax: max boundary of scale
    :param preference_direction: scale preference direction
    :raises ValueError:
        * if `dmax` smaller than `dmin`
        * if `preference_direction` is unknown
    """

    def __init__(
        self,
        dmin: NumericValue,
        dmax: NumericValue,
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ):
        """Constructor method"""
        Interval.__init__(self, dmin, dmax)
        if not PreferenceDirection.has_value(preference_direction):
            raise ValueError(PreferenceDirection.content_message())
        self.preference_direction = preference_direction

    def __contains__(self, x: Value) -> bool:
        """Check if values are inside scale.

        :param x:
        :return:
        """
        return self.inside(cast(NumericValue, x))

    def normalize(self, x: NumericValue) -> NumericValue:
        """Normalize numeric value.

        :param x:
        :return:

        .. note::
            `preference_direction` is taken into account, so preferred
            value is always bigger.
        """
        if self.preference_direction == PreferenceDirection.MIN:
            return 1 - Interval.normalize(self, x)
        return Interval.normalize(self, x)


class QualitativeScale(QuantitativeScale, NominativeScale):
    """This class implements a MCDA qualitative scale.

    :param labels:
    :param values:
    :param preference_direction: scale preference direction
    :raises ValueError:
        * if number of `labels` and `values` differs
        * if `preference_direction` is unknown
    :raises TypeError:
        * if `values` contains non-numeric values
    """

    def __init__(
        self,
        labels: List[Value],
        values: List[NumericValue],
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ):
        """Constructor method"""
        if len(labels) != len(values):
            raise ValueError(
                "QualitativeScale must have same number of labels"
                " and values"
            )
        NominativeScale.__init__(self, labels)
        for value in values:
            if type(value) not in [
                int,
                float,
                np.float,
                np.int,
            ]:
                raise TypeError(
                    "QualitativeScale must have numeric values."
                    f"Got: {type(value)}"
                )
        self.values = values
        QuantitativeScale.__init__(
            self,
            min(self.values),
            max(self.values),
            preference_direction,
        )

    def __contains__(self, x: Value) -> bool:
        """Check if label is inside scale.

        :param x:
        :return:
        """
        return NominativeScale.__contains__(self, x)

    def transform(self, x: Value) -> NumericValue:
        """Return value corresponding to given label.

        :param x:
        :raises ValueError: if `x` is an unknown label
        :return:
        """
        if x not in self:
            raise ValueError(f"unknown label: {x}")
        return self.values[self.labels.index(x)]


class FuzzyScale(QualitativeScale):
    """This class implements a MCDA fuzzy qualitative scale.

    :param labels:
    :param fuzzy:
    :param preference_direction: scale preference direction
    :raises ValueError:
        * if number of `labels` and `fuzzy` differs
        * if `preference_direction` is unknown
    :raises TypeError:
        * if `fuzzy` contains non-fuzzy numbers
    """

    def __init__(
        self,
        labels: List[Value],
        fuzzy: List[FuzzyNumber],
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ):
        values = []
        for fz in fuzzy:
            if type(fz) is not FuzzyNumber:
                raise TypeError("fuzzy scales can only contains fuzzy numbers")
            values.append(fz.average())
        QualitativeScale.__init__(self, labels, values, preference_direction)
        self.fuzzy = fuzzy


def try_transform_value(label: Value, scale: Scale) -> Value:
    """Transform label if the scale is qualitative.

    :param label:
    :param scale:
    :return:
    """
    return (
        scale.transform(label)
        if isinstance(scale, QualitativeScale)
        else label
    )


def try_normalize_value(value: Value, scale: Scale) -> Value:
    """Normalize numeric value if the scale is quantitative.

    :param value:
    :param scale:
    :return:

    .. note::
        labels of :class:`QualitativeScale` must be transformed beforehand
    """
    return (
        scale.normalize(cast(NumericValue, value))
        if isinstance(scale, QuantitativeScale)
        else value
    )


class VectorizedScale(Scale):
    """Basic abstract class for vectorized MCDA scale."""

    def __init__(self):
        """Constructor method"""
        self._inside = VectorizedFunction({}, self._inside_single)
        self._transform = VectorizedFunction({}, self._transform_single)

    def __contains__(self, x: Value) -> bool:
        """Check if values are inside scale.

        :param x:
        :return:
        """
        return self._inside_single(x)

    def inside(self, x: Any) -> bool:
        """Check if values are inside scale.

        :param x:
        :return:
        """
        return self._inside(x)

    def transform(self, x: Any) -> Value:
        """Return values if within scale.

        :param x:
        :raises ValueError: if any value is outside scale
        :return:
        """
        return self._transform(x)

    def _inside_single(self, x: Value) -> bool:
        """Check if value is inside scale.

        :param x:
        :return:
        """
        return False

    def _transform_single(self, x: Value) -> Value:
        """Return value if within scale.

        :param x:
        :raises ValueError: if `x` is outside scale
        :return:
        """
        if self._inside(x):
            return x
        raise ValueError(f"{x} outside scale")

    def normalize(self, x: NumericValue) -> NumericValue:
        """Normalize value.

        :param x:
        :return:
        """
        return x


class VectorizedNominativeScale(VectorizedScale, NominativeScale):
    """This class implements a vectorized MCDA nominative scale.

    :param labels:
    """

    def __init__(self, labels: List[Value]):
        """Constructor method"""
        VectorizedScale.__init__(self)
        NominativeScale.__init__(self, labels)

    def _inside_single(self, x: Value) -> bool:
        """Check if value is inside scale.

        :param x:
        :return:
        """
        return x in self.labels


class VectorizedQuantitativeScale(VectorizedScale, QuantitativeScale):
    """This class implements a vectorized MCDA quantitative scale.

    :param dmin: min boundary of scale
    :param dmax: max boundary of scale
    :param preference_direction: scale preference direction
    :raises ValueError:
        * if `dmax` smaller than `dmin`
        * if `preference_direction` is unknown
    """

    def __init__(
        self,
        dmin: NumericValue,
        dmax: NumericValue,
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ):
        """Constructor method"""
        VectorizedScale.__init__(self)
        QuantitativeScale.__init__(self, dmin, dmax, preference_direction)

    def _inside_single(self, x: Value) -> bool:
        """Check if value is inside scale.

        :param x:
        :return:
        """
        return self.dmin <= cast(NumericValue, x) <= self.dmax

    def normalize(self, x: NumericValue) -> NumericValue:
        """Normalize value.

        :param x:
        :return:
        """
        return cast(NumericValue, self._transform_single(x)) / (
            self.dmax - self.dmin
        )


class VectorizedQualitativeScale(VectorizedNominativeScale):
    """This class implements a vectorized MCDA qualitative scale.

    :param labels:
    :param values:
    :param preference_direction: scale preference direction
    :raises ValueError:
        * if number of `labels` and `values` difer
        * if `preference_direction` is unknown
    :raises TypeError:
        * if `values` contains non-numeric values
        * if `values` mixes numerics with :class:`pymcda.functions.FuzzyNumber`
    """

    def __init__(
        self,
        labels: List[Value],
        values: List[Union[NumericValue, FuzzyNumber]],
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ):
        """Constructor method"""
        if len(labels) != len(values):
            raise ValueError(
                "QualitativeScale must have same number of labels"
                " and values"
            )
        VectorizedNominativeScale.__init__(self, labels)
        is_fuzzy_scale = type(values[0]) in [
            VectorizedFuzzyNumber,
            FuzzyNumber,
        ]
        for value in values:
            if type(value) not in [
                int,
                float,
                np.float,
                np.int,
                FuzzyNumber,
                VectorizedFuzzyNumber,
            ]:
                raise TypeError(
                    "QualitativeScale must have numeric values."
                    f"Got: {type(value)}"
                )
            if is_fuzzy_scale != (type(value) is VectorizedFuzzyNumber):
                raise TypeError(
                    "QualitativeScale cannot mix single numeric "
                    "values and fuzzy numbers"
                )
        self.values = values
        if not PreferenceDirection.has_value(preference_direction):
            raise ValueError(PreferenceDirection.content_message())
        self.preference_direction = preference_direction

    def _inside_single(self, x: Value) -> bool:
        """Check if value is inside scale.

        :param x:
        :return:
        """
        return VectorizedNominativeScale._inside_single(self, x)

    def _transform_single(self, x: Value) -> Value:
        """Return associated value of given label if within scale.

        :param x:
        :raises ValueError: if `x` is outside scale
        :return:
        """
        try:
            i = self.labels.index(x)
            return numeric_value(self.values[i])
        except ValueError:
            raise ValueError(f"{x} outside scale")

    def transform(self, x: Any) -> Any:
        """Return associated value if labels are within scale.

        :param x: labels
        :raises ValueError: if any value is outside scale
        :return:
        """
        return self._transform(x)
