"""Day 11

Order of the stones doesn't matter, so we can use a dictionary to keep track of them
That way we can "step" every stone with the same number all at once
lru_cache for good measure but it's not necessary
"""

# pylint: disable=invalid-name, redefined-outer-name

from collections import defaultdict
from functools import lru_cache
from utils.inputs import get_input

DAY = 11


def step_stones_dict(stones_dict: dict) -> dict:
    """Return the stones_dict after one step (one blink)"""
    new_stones_dict = defaultdict(int)
    for stone, count in stones_dict.items():
        _new_stones = step_stone(stone)
        for _stone in _new_stones:
            new_stones_dict[_stone] += count
    return new_stones_dict


@lru_cache
def step_stone(stone: int) -> list[int]:
    """Return the result of a step on a single stone"""
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        k = len(stone_str) // 2
        return [int(stone_str[:k]), int(stone_str[k:])]
    return [2024 * stone]


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse input into a dictionary of stones
    # keys = stones, values = counts
    stones = [int(x) for x in s.strip().split()]
    stones_dict = defaultdict(int)
    for stone in stones:
        stones_dict[stone] += 1

    # do the steps
    for _ in range(25):
        stones_dict = step_stones_dict(stones_dict)

    return sum(stones_dict.values())


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    # parse input into a dictionary of stones
    # keys = stones, values = counts
    stones = [int(x) for x in s.strip().split()]
    stones_dict = defaultdict(int)
    for stone in stones:
        stones_dict[stone] += 1

    # do the steps
    for _ in range(75):
        stones_dict = step_stones_dict(stones_dict)

    return sum(stones_dict.values())


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
