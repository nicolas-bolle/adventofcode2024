"""Day 1"""


# pylint: disable=invalid-name, redefined-outer-name

import numpy as np
import pandas as pd

from utils.inputs import get_input

DAY = 1


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    array = np.array(list(map(int, s.strip().split()))).reshape(-1, 2)
    l1 = sorted(array[:, 0])
    l2 = sorted(array[:, 1])
    soln = sum(abs(np.array(l1) - np.array(l2)))
    return soln


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    array = np.array(list(map(int, s.strip().split()))).reshape(-1, 2)

    l1 = list(array[:, 0])
    l2 = list(array[:, 1])

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
