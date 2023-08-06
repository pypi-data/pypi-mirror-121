from typing import List, Tuple, Union
import numpy as np

_EPS = 1e-8


def _times(a, b):
    cnt = 0

    while a - b > _EPS:
        a -= b
        cnt += 1
    return cnt


def hist(array: List[Union[int, float]],
              bins: int) -> Tuple[List[int], List[float]]:
    """
    Builds bins' labels and bins' value counts for given array
    :param array: array with numeric values
    :param bins:  number of bins in result distribution
    :return: Two lists:
             first contains value counts of each bin,
             second contains list of bins' labels
    """

    minn, maxx = min(array), max(array)
    step = (maxx - minn) / bins
    bins_names = list(np.arange(minn, maxx, step))

    bins_val = [0] * len(bins_names)
    for el in array:
        bins_val[_times(el - minn, step)] += 1
    return bins_val, bins_names
