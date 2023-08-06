from typing import List, Tuple, Union
from math import floor
import numpy as np
import matplotlib.pyplot as plt

def fast_hist(array: List[Union[int, float]], 
              bins: int) -> Tuple[List[int], List[float]]:
    if bins <= 0:
        raise ValueError("bins count must be positive")
    minValue = min(array)
    maxValue = max(array)
    binSize = (maxValue - minValue) / bins
    value_counts = np.zeros((bins))
    bins_names = np.linspace(minValue, maxValue, bins + 1)
    for val in array:
      value_counts[min(bins - 1, floor((val - minValue) / binSize))] += 1
    plt.bar(bins_names[:-1], value_counts, align='edge', width=binSize * 0.9)
    return (value_counts, bins_names)