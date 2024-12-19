"""Day 19

Part 1: initially I did a depth first search
Part 2: I modified my part 1 solution into dynamic programming
And then I went back and changed my solution for part 1 to use the one for part 2
"""

# pylint: disable=invalid-name, redefined-outer-name

from functools import cache

from utils.inputs import get_input

DAY = 19


def parse_input(s: str) -> tuple[list[str], list[str]]:
    """Parse input into lists of towels and designs"""
    towels, designs = tuple(s.strip().split("\n\n"))
    towels = towels.replace(",", "").split()
    designs = designs.split()
    return towels, designs


@cache
def count_ways(design: str, towels: tuple[str]) -> bool:
    """Count how many ways it's possible to build the given design out of the given towels
    Dynamic programming via recursion + caching
    towels must be a tuple of strings so it's hashable for the caching
    """
    if design == "":
        return 1
    ways = 0
    for towel in towels:
        if design.startswith(towel):
            _ways = count_ways(design.removeprefix(towel), towels)
            ways += _ways
    return ways


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse
    towels, designs = parse_input(s)

    # count_ways() needs things so it's able to hash the input
    towels = tuple(towels)

    # count up how many designs can be made in at least one way
    return sum(count_ways(design, towels) > 0 for design in designs)


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    towels, designs = parse_input(s)
    towels = tuple(towels)
    return sum(count_ways(design, towels) for design in designs)


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
