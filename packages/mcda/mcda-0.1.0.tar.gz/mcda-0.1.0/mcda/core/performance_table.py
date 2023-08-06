from typing import List, Union, cast

from .aliases import (
    Function,
    NumericPerformanceTable,
    NumericValue,
    PerformanceTable,
    Value,
)
from .scales import Scale, try_normalize_value, try_transform_value


def is_numeric(performance_table: PerformanceTable) -> bool:
    """Check whether performance table is numeric.

    :param performance_table:
    :return:
    :rtype: bool
    """
    for row in performance_table:
        for cell in row:
            if type(cell) not in [int, float]:
                return False
    return True


def apply_criteria_functions(
    performance_table: PerformanceTable, functions: List[Function]
) -> PerformanceTable:
    """Apply criteria functions to performance table and return result.

    :param performance_table:
    :param functions: list of functions in same criteria order than table
    :return:
    """
    return [
        [f(perf) for f, perf in zip(functions, aPerf)]
        for aPerf in performance_table
    ]


def apply_criteria_weights(
    performance_table: NumericPerformanceTable, weights: List[NumericValue]
) -> NumericPerformanceTable:
    """Apply criteria weights to a numeric performance table and return result.

    :param performance_table:
    :param weights: criteria weights in same criteria order than table
    :return:
    """
    return [
        [w * perf for w, perf in zip(weights, aPerf)]
        for aPerf in performance_table
    ]


def transform(
    performance_table: PerformanceTable, scales: List[Scale]
) -> PerformanceTable:
    """Apply scale transform method to performance table and return result.

    :param performance_table:
    :param scales:
    :return:

    .. note::
        Only :class:`QualitativeScale` will transform labels into
        numeric values
    """
    return [
        [
            try_transform_value(perf, scale)
            for perf, scale in zip(aPerf, scales)
        ]
        for aPerf in performance_table
    ]


def get_performances(
    performance_table: PerformanceTable, index: int, axis: int = 0
) -> List[Value]:
    """Get performance row or column.

    Behaviour depends on `axis` value:

    * ``0``: returns performances on row `index`
    * ``1``: returns performances on column `index`

    :param performance_table:
    :param index: row/column index
    :param axis: determines dimension to return
    :return:
    """
    if axis == 0:
        return performance_table[index]
    return [perf[index] for perf in performance_table]


def get_alternative_values(
    performance_table: PerformanceTable, index: int
) -> List[Value]:
    """Get performances associated to an alternative.

    :param performance_table:
    :param index: alternative index
    :return:
    """
    return get_performances(performance_table, index, axis=0)


def get_criterion_values(
    performance_table: PerformanceTable, index: int
) -> List[Value]:
    """Get performances associated to a criterion.

    :param performance_table:
    :param index: criterion index
    :return:
    """
    return get_performances(performance_table, index, axis=1)


def normalize(
    performance_table: PerformanceTable, axis: int = 0
) -> NumericPerformanceTable:
    """Normalize performance table along given axis.

    `axis` parameter changes what is returned:

    * ``0``: normalization is done per criterion
    * ``1``: normalization is done per alternative

    :param performance_table:
    :param axis:
    :return:
    """
    if not is_numeric(performance_table):
        raise ValueError("Only numeric performance tables can be normalized")
    _performance_table = cast(NumericPerformanceTable, performance_table)
    if axis == 0:
        values = [
            [_performance_table[i][j] for i in range(len(_performance_table))]
            for j in range(len(_performance_table[0]))
        ]
        min_values = [min(v) for v in values]
        max_values = [max(v) for v in values]
        return [
            [
                (_performance_table[i][j] - minv) / (maxv - minv)
                for j, minv, maxv in zip(
                    range(len(min_values)), min_values, max_values
                )
            ]
            for i in range(len(_performance_table))
        ]
    min_values = [min(v) for v in _performance_table]
    max_values = [max(v) for v in _performance_table]
    return [
        [(p - minv) / (maxv - minv) for p in perf]
        for perf, minv, maxv in zip(_performance_table, min_values, max_values)
    ]


def normalize_with_scales(
    performance_table: PerformanceTable, scales: List[Scale]
) -> PerformanceTable:
    """Normalize performance table using criteria scales.

    :param performance_table:
    :param scales:
    :return:

    .. note:: labels from :class:`scales.NominativeScale` won't be changed
    .. warning::
        :class:`scales.QualitativeScale` labels must have been first
        transformed into corresponding values (e.g calling :func:`transform`
        first)
    """
    return [
        [
            try_normalize_value(perf, scale)
            for perf, scale in zip(aPerf, scales)
        ]
        for aPerf in performance_table
    ]


def is_within_criteria_scales(
    performance_table: PerformanceTable, scales: List[Scale]
) -> bool:
    """Check whether all cells are within their respective criteria scales.

    :param performance_table:
    :param scales:
    :return:
    """
    for j, s in enumerate(scales):
        for aPerf in performance_table:
            if not aPerf[j] in s:
                return False
    return True


def sum_table(
    performance_table: PerformanceTable, axis: int = None
) -> Union[List[NumericValue], NumericValue]:
    """Sum performances.

    Behaviour depends on `axis` value:

    * ``0``: returns column sums as a list
    * ``1``: returns row sums as a list
    * else: returns sum on both dimension as a numeric value

    :param performance_table:
    :param axis: axis on which the sum is made
    :return:
    """
    if not is_numeric(performance_table):
        raise ValueError("Can only sum numeric performance table")
    _performance_table = cast(NumericPerformanceTable, performance_table)
    if axis == 1:
        return [sum(aPerf) for aPerf in _performance_table]
    elif axis == 0:
        return [
            sum([aPerf[j] for aPerf in _performance_table])
            for j in range(len(_performance_table[0]))
        ]
    else:
        return sum([sum(aPerf) for aPerf in _performance_table])
