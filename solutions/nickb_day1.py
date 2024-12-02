"""Day 1"""


# pylint: disable=unused-import, invalid-name

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
    soln = "TODO"
    return soln


def solution_part2(s: str):
    """Part 2 solution from the plaintext input"""
    soln = "TODO"
    return soln


if __name__ == "main":
    s = get_input(DAY)
    soln1 = solution_part1(s)
    print("Part 1 solution:")
    print(soln1)
    print()
    soln2 = solution_part2(s)
    print("Part 2 solution:")
    print(soln2)
    print()
    print("Done")
