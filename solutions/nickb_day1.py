"""Day 1"""


# pylint: disable=unused-import, invalid-name, redefined-outer-name

from abc import ABC, abstractmethod
from functools import lru_cache

import re
from collections import deque
import numpy as np
import pandas as pd

from utils.inputs import (
    get_input,
    split,
    split_newline,
    split_lax,
    list_map,
    list_reshape,
    get_int,
    get_float,
)

DAY = 1


def solution_part1(s: str):
    """Part 1 solution from the plaintext input"""
    aux = np.array(list_map(get_int, split_lax(s))).reshape(-1, 2)
    l1 = sorted(aux[:, 0])
    l2 = sorted(aux[:, 1])
    soln = sum(abs(np.array(l1) - np.array(l2)))
    return soln


def solution_part2(s: str):
    """Part 2 solution from the plaintext input"""
    aux = np.array(list_map(get_int, split_lax(s))).reshape(-1, 2)

    l1 = list(aux[:, 0])
    l2 = list(aux[:, 1])

    l1_counts = pd.Series(l1).value_counts()
    l2_counts = pd.Series(l2).value_counts()
    idx = l1_counts.index.intersection(l2_counts.index)
    l1_counts = l1_counts[idx]
    l2_counts = l2_counts[idx]

    soln = (idx * l1_counts * l2_counts).sum()

    return soln


if __name__ == "__main__":
    s = get_input(DAY)
    print()
    soln1 = solution_part1(s)
    print("Part 1 solution:")
    print(soln1)
    print()
    soln2 = solution_part2(s)
    print("Part 2 solution:")
    print(soln2)
    print()
    print("Done")
