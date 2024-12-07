"""Day 3"""


# pylint: disable=invalid-name, redefined-outer-name

import re

from utils.inputs import get_input

DAY = 3


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    expr = r"mul\(([0-9]+),([0-9]+)\)"
    res = re.findall(expr, s)

    c = 0
    for a, b in res:
        c = c + int(a) * int(b)

    return c


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    expr = r"mul\(([0-9]+),([0-9]+)\)|(do\(\))|(don't\(\))"
    res = re.findall(expr, s)

    c = 0
    enabled = True
    for a, b, _do, _dont in res:
        if _do:
            enabled = True
            continue
        if _dont:
            enabled = False
            continue
        if enabled:
            c = c + int(a) * int(b)

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
