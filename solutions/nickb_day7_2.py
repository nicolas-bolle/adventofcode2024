"""Day 7

Faster solution (4 seconds) doing it recursively with pruning
"""

# pylint: disable=invalid-name, redefined-outer-name

from collections import deque

from utils.inputs import get_input

DAY = 7


def parse_line(line):
    """Parse a line, ex. "190: 10 19" to (190, 10, 19)"""
    return tuple(map(int, line.replace(":", "").split(" ")))


def plus(a, b):
    return a + b


def times(a, b):
    return a * b


def concat(a, b):
    return int(str(a) + str(b))


OPS1 = [plus, times]
OPS2 = [plus, times, concat]


def check_solvable(num: int, remaining_nums: deque, ops: list[str], target: int):
    """Check if from num we can get to target with the remaining nums using operations from ops
    Recursive, with pruning if we overshoot the target (valid since the operations are "monotonic" because the input doesn't have 0s)
    """
    # base case
    if len(remaining_nums) == 0:
        return num == target

    # pruning if we overshot the target
    if num > target:
        return False

    # recursive step, modifying deque in place to avoid the time cost of copying a list
    num2 = remaining_nums.popleft()
    for op in ops:
        if check_solvable(op(num, num2), remaining_nums, ops, target):
            return True
    remaining_nums.appendleft(num2)
    return False


def solution_part1(s: str):
    """Part 1 solution from the plaintext input"""
    lines = list(map(parse_line, s.strip().split("\n")))

    # confirming no lines have zeros, so the pruning in check_solvable() is valid
    assert min(map(min, lines)) > 0

    c = 0
    for line in lines:
        if check_solvable(line[1], deque(line[2:]), OPS1, line[0]):
            c = c + line[0]

    return c


def solution_part2(s: str):
    """Part 2 solution from the plaintext input"""
    lines = list(map(parse_line, s.strip().split("\n")))

    # confirming no lines have zeros, so the pruning in check_solvable() is valid
    assert min(map(min, lines)) > 0

    c = 0
    for line in lines:
        if check_solvable(line[1], deque(line[2:]), OPS2, line[0]):
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
