"""Day 2"""


# pylint: disable=invalid-name, redefined-outer-name

import numpy as np

from utils.inputs import get_input

DAY = 2


def parse_line(line):
    return [int(x) for x in line.split()]


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    p = [parse_line(line) for line in s.strip().split("\n")]
    soln = sum(is_safe(line) for line in p)
    return soln


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    p = [parse_line(line) for line in s.strip().split("\n")]
    soln = sum(is_safe_dampened(line) for line in p)
    return soln


def is_safe(row):
    diffs = np.diff(np.array(row))
    return (
        (all(diffs >= 0) or all(diffs <= 0))
        and all(abs(diffs) >= 1)
        and all(abs(diffs) <= 3)
    )


def is_safe_dampened(row):
    return any(is_safe(row[:i] + row[i + 1 :]) for i in range(len(row)))


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
