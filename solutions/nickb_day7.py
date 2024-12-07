"""Day 7

Takes 30 seconds
I just iterate over all possible sets of operations and test them one by one
Ex. for part 1 if the numbers are 81, 40, 27, then the possible operations are:
+ +
+ *
* +
* *

(If a set of operations works, we don't have to check the rest)

Part 2 is the same but allowing for the || operation
So in the example there are 9 possible sets of operations

This means the worst case ends up being 3**13 = 1_594_323 sets of operations for the longest lines
Which slows things down but doesn't make things infeasible
"""


# pylint: disable=unused-import, invalid-name, redefined-outer-name

from abc import ABC, abstractmethod
from functools import lru_cache

import re
import itertools
from collections import deque, defaultdict
from frozendict import frozendict
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

DAY = 7


def parse_line(line):
    """Parse a line, ex. "190: 10 19" to [190, 10, 19]"""
    return tuple(map(int, line.replace(":", "").split(" ")))


VALID_OPS1 = ["+", "*"]
VALID_OPS2 = ["+", "*", "||"]


def solve_line(line, valid_ops):
    """Check if some combination of operations "solves" the line"""
    target = line[0]
    numbers = line[1:]
    for ops in itertools.product(valid_ops, repeat=len(numbers) - 1):
        if check_math(numbers, ops, target):
            return True
    return False


def check_math(numbers, ops, target):
    """Check if the math works out for a set of operations"""
    val = numbers[0]
    for n, op in zip(numbers[1:], ops):
        match op:
            case "+":
                val = val + n
            case "*":
                val = val * n
            case "||":
                val = int(str(val) + str(n))
    return val == target


def solution_part1(s: str):
    """Part 1 solution from the plaintext input"""
    lines = list(map(parse_line, s.strip().split("\n")))
    c = 0
    for line in lines:
        if solve_line(line, VALID_OPS1):
            c = c + line[0]
    return c


def solution_part2(s: str):
    """Part 2 solution from the plaintext input"""
    lines = list(map(parse_line, s.strip().split("\n")))
    c = 0
    for line in lines:
        if solve_line(line, VALID_OPS2):
            c = c + line[0]
    return c


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
