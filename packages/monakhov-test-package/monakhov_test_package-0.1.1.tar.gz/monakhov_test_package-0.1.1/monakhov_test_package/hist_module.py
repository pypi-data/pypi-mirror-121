from typing import List, Tuple, Union
import numpy as np

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
        bins_val[min(int((el - minn) / step), bins - 1)] += 1
    return bins_val, bins_names
