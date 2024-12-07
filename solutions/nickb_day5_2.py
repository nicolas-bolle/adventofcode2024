"""Day 5

Copied the idea from Marcus Huerta
https://github.com/KMX-Advent-of-Code/2024-Advent-of-Code/blob/main/Day5/MarcosDay5.py

Use Page objects to implement comparison sorting for part 2
"""

# pylint: disable=invalid-name, redefined-outer-name

# TODO standardize these imports
from typing import Self
from functools import total_ordering

from utils.inputs import get_input

DAY = 5


@total_ordering
class Page:
    """Represents a page in a printing"""

    # the rules set to use for comparisons
    rules = set()

    def __init__(self, n: int, rules: set):
        self.n = n
        self.rules = rules

    def __eq__(self, other: Self):
        """Check page equality"""
        return self.n == other.n

    def __lt__(self, other: Self):
        """Compare to another page
        Ensure the pages are comparable
        """
        if (self.n, other.n) in self.rules:
            return True
        if self == other:
            return False
        if (other.n, self.n) in self.rules:
            return False
        return NotImplemented


def parse_rule(x: str) -> tuple[int, int]:
    """Convert the string 'a|b' to the tuple of ints (a, b)"""
    return tuple(int(t) for t in x.split("|"))


def parse_printing(x: str, rules) -> list[Page]:
    """Convert the string 'a,b,c' to a list of Pages"""
    return [Page(int(t), rules) for t in x.split(",")]


def get_middle_page_value(printing: list[Page]):
    """Get the middle page value of a printing"""
    n = len(printing)
    assert n % 2 == 1
    return printing[n // 2].n


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse into rules and printings
    # rules: set of tuples (a, b)
    # printings: list of Pages
    rules, printings = tuple(s.strip().split("\n\n"))
    rules = {parse_rule(line) for line in rules.split("\n")}
    printings = [parse_printing(line, rules) for line in printings.split("\n")]

    # count up the sum of middle pages in valid printings
    c = 0
    for printing in printings:
        if printing == sorted(printing):
            val = get_middle_page_value(printing)
            c = c + val

    return c


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    rules, printings = tuple(s.strip().split("\n\n"))
    rules = {parse_rule(line) for line in rules.split("\n")}
    printings = [parse_printing(line, rules) for line in printings.split("\n")]

    # count up the sum of middle pages in sorted invalid printings
    c = 0
    for printing in printings:
        printing_sorted = sorted(printing)
        if printing != printing_sorted:
            val = get_middle_page_value(printing_sorted)
            c = c + val

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
