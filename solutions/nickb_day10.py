"""Day 10

Part 2 was a dynamic programming kind of thing
lru_cache made coding it up straightforward as a recursive kind of thing
"""

# pylint: disable=invalid-name, redefined-outer-name

from functools import lru_cache
import numpy as np
from utils.inputs import get_input

DAY = 10


def spread(A: np.ndarray, h: int, locs: set[tuple[int, int]]):
    """For part 1
    Spread the set of locations at height h to locations with height h + 1
    """
    n, m = A.shape
    locs_new = set()
    for i, j in locs:
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            _i, _j = i + di, j + dj
            if (0 <= _i < n) and (0 <= _j < m) and (A[_i, _j] == h + 1):
                locs_new.add((i + di, j + dj))
    return locs_new


@lru_cache
def calc_rating(A: tuple[tuple], i: int, j: int):
    """For part 2
    The rating of location (i, j) in A
    Computed recursively (with caching)
    If (i, j) is at height h < 9, its rating is the sum of the
        ratings of the trails it can branch to
    """
    h = A[i][j]

    # base case (end of a trail)
    if h == 9:
        return 1

    n = len(A)
    m = len(A[0])

    # recursive step
    rating = 0
    for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        _i, _j = i + di, j + dj
        if (0 <= _i < n) and (0 <= _j < m) and (A[_i][_j] == h + 1):
            rating += calc_rating(A, _i, _j)

    return rating


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # make it a numpy array
    A = np.array([list(map(int, line)) for line in s.strip().split("\n")])

    # a list of tuples (i, j) of coords of zeros (trailheads)
    idx_zeros = [(int(i), int(j)) for i, j in zip(*np.where(A == 0))]

    # count up the scores
    total_score = 0
    for i, j in idx_zeros:
        locs = {(i, j)}
        for h in range(9):
            locs = spread(A, h, locs)
        trailhead_score = len(locs)
        total_score += trailhead_score

    return total_score


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    A = np.array([list(map(int, line)) for line in s.strip().split("\n")])
    idx_zeros = [(int(i), int(j)) for i, j in zip(*np.where(A == 0))]

    # hashable version of A so lru_cache is happy
    A_hashable = tuple([tuple([int(x) for x in row]) for row in A])

    total_rating = 0
    for i, j in idx_zeros:
        trailhead_rating = calc_rating(A_hashable, i, j)
        total_rating += trailhead_rating

    return total_rating


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
