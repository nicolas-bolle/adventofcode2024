"""Day 5
Required a lot of helper functions
The helper functions for part 1 aren't too weird
But for part 2 I made reorder_printing() and digraph_longest_path_length() which are fancier
This is because I solved part 2 by viewing it as finding the longest path in a digraph
Viewing rules as directed edges on the graph of pages,
    for each printing we look at the induced digraph
And the longest path can be found by ordering the printing according to the
    length of the longest path from each page (in descending order)
"""


# pylint: disable=unused-import, invalid-name, redefined-outer-name

from abc import ABC, abstractmethod
from functools import lru_cache

import re
from collections import deque
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

DAY = 5


def parse_rule(x: str) -> tuple[int, int]:
    """Convert the string 'a|b' to the tuple of ints (a, b)"""
    return tuple([int(t) for t in x.split("|")])


def parse_printing(x: str) -> list[int]:
    """Convert the string 'a,b,c' to the list of ints [a, b, c]"""
    return [int(t) for t in x.split(",")]


def check_valid_printing(printing: list[int], rules: set[tuple[int, int]]) -> bool:
    """Check a printing is valid under the rule set"""
    # iterate over ordered pairs (a, b) of pages in the printing
    # if the order violates a rule (i.e. the rule (b, a)), mark the printing as invalid
    for i, a in enumerate(printing):
        for b in printing[i + 1 :]:
            if (b, a) in rules:
                return False

    # assume valid unless found otherwise
    return True


def get_middle_page_of_printing(printing: list[int]):
    """Get the middle page of a printing"""
    n = len(printing)
    assert n % 2 == 1
    return printing[n // 2]


def reorder_printing(printing: list[int], rules: set[tuple[int, int]]) -> list[int]:
    """Reorder a printing following the rules
    Done by
    - Subsetting the rules to those involving the pages of the printing
    - Finding a max length path in the implied digraph
    """
    # subset to relevant rules, formatted as a dictionary of forward edges
    # frozendict with tuple keys so caching works for digraph_longest_path_length()
    _rules = [
        rule for rule in list(rules) if rule[0] in printing and rule[1] in printing
    ]
    rules_dict = {page: [] for page in printing}
    for a, b in _rules:
        rules_dict[a].append(b)
    for key, val in rules_dict.items():
        rules_dict[key] = tuple(val)
    rules_dict = frozendict(rules_dict)

    # find longest path lengths
    printing_tuple = tuple(printing)
    path_lengths = [
        digraph_longest_path_length(page, rules_dict, printing_tuple)
        for page in printing
    ]

    # order by the longest path lengths, in descending order
    series = pd.Series(path_lengths, index=printing)
    series.sort_values(ascending=False, inplace=True)
    return list(series.index)


@lru_cache
def digraph_longest_path_length(page: int, rules_dict: frozendict, printing_tuple):
    """Find the length of the longest path starting at the given page under the rule set
    Works recursively, caching since otherwise the speed would be horrible
    Printing tuple is a passthrough arg just to make sure nothing funny happens with the caching
    """
    children = rules_dict[page]
    if len(children) == 0:
        return 1
    return (
        max(
            [
                digraph_longest_path_length(child, rules_dict, printing_tuple)
                for child in children
            ]
        )
        + 1
    )


def solution_part1(s: str):
    """Part 1 solution from the plaintext input"""
    # parse into rules and printings
    # rules: set of tuples (a, b) for the rules
    # printings: list of lists [a, b, c, ...] for the printings
    rules, printings = tuple(split(s, "\n\n"))
    rules = set(list_map(parse_rule, split_newline(rules)))
    printings = list_map(parse_printing, split_newline(printings))

    # count up the sum of middle pages in valid printings
    c = 0
    for printing in printings:
        if check_valid_printing(printing, rules):
            middle_page = get_middle_page_of_printing(printing)
            c = c + middle_page

    return c


def solution_part2(s: str):
    """Part 2 solution from the plaintext input"""
    rules, printings = tuple(split(s, "\n\n"))
    rules = set(list_map(parse_rule, split_newline(rules)))
    printings = list_map(parse_printing, split_newline(printings))

    # count up the sum of middle pages in reordered invalid printings
    c = 0
    for printing in printings:
        if not check_valid_printing(printing, rules):
            _printing = reorder_printing(printing, rules)
            middle_page = get_middle_page_of_printing(_printing)
            c = c + middle_page

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
