"""Day 8

The key things were
- Grouping antennas by frequency
- Using gcd in part 2
"""

# pylint: disable=invalid-name, redefined-outer-name

import itertools
from collections import defaultdict
import math
import numpy as np

from utils.inputs import get_input

DAY = 8


def parse_input(s: str) -> tuple[int, int, dict]:
    """Parse the input into a dictionary giving antenna locations for each frequency
    Plus the dimensions of the grid
    antennas[freq] gives a list of locations (i, j) of antennas at that frequency
    """
    A = np.array([list(line) for line in s.strip().split("\n")])
    n, m = A.shape

    antennas = defaultdict(list)
    for i in range(n):
        for j in range(m):
            c = str(A[i, j])
            if c != ".":
                antennas[c].append((i, j))

    return n, m, antennas


def get_antinodes1(i1, j1, i2, j2, n, m) -> set:
    """Get antinodes for antennas of the same frequency at (i1, j1), (i2, j2)
    Limits coords to the n x m grid
    """
    _i1 = 2 * i1 - i2
    _j1 = 2 * j1 - j2
    _i2 = 2 * i2 - i1
    _j2 = 2 * j2 - j1

    antinodes = set()

    if (0 <= _i1 < n) and (0 <= _j1 < m):
        antinodes.add((_i1, _j1))
    if (0 <= _i2 < n) and (0 <= _j2 < m):
        antinodes.add((_i2, _j2))

    return antinodes


def get_antinodes2(i1, j1, i2, j2, n, m) -> set:
    """get_antinodes1 but like for part 2
    The key thing is dividing by the gcd so we hit all grid points
    """
    # vector for finding antinodes at grid points
    vi, vj = i2 - i1, j2 - j1
    d = math.gcd(vi, vj)
    vi, vj = vi // d, vj // d

    # "base" antinode
    antinodes = {(i1, j1)}

    # add nodes in the "positive direction"
    i, j = i1, j1
    while True:
        i, j = i + vi, j + vj
        if not ((0 <= i < n) and (0 <= j < m)):
            break
        antinodes.add((i, j))

    # add nodes in the "negative direction"
    i, j = i1, j1
    while True:
        i, j = i - vi, j - vj
        if not ((0 <= i < n) and (0 <= j < m)):
            break
        antinodes.add((i, j))

    return antinodes


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    n, m, antennas = parse_input(s)

    antinodes = set()

    # iterate over pairs of antennas with the same frequency
    for locs in antennas.values():
        for (i1, j1), (i2, j2) in itertools.combinations(locs, 2):
            # add the antinodes they generate
            antinodes.update(get_antinodes1(i1, j1, i2, j2, n, m))

    return len(antinodes)


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    n, m, antennas = parse_input(s)

    antinodes = set()

    # iterate over pairs of antennas with the same frequency
    for locs in antennas.values():
        for (i1, j1), (i2, j2) in itertools.combinations(locs, 2):
            # add the antinodes they generate
            antinodes.update(get_antinodes2(i1, j1, i2, j2, n, m))

    return len(antinodes)


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
