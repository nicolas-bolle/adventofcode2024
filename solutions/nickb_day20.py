"""Day 20

Takes 5 seconds

I compute the distance of each location to the end, so that to "judge" each possible cheat
    you just have to look at the distance of the start and end locations of the cheat

In part 1 I originally had the "cheat moves" hardcoded as (0, 2), (0, -2), (2, 0), (-2, 0),
    and for part 2 realized this could be generalized to an arbitrary radius of cheat moves

Also, I should probably make standard utils for things like array parsing and shortest distances
    instead of manually coding them each time
"""

# pylint: disable=invalid-name, redefined-outer-name

from collections import defaultdict
import numpy as np
import pandas as pd

from utils.inputs import get_input

DAY = 20


def parse_array(s: str) -> np.ndarray:
    """Parse the input into a numpy array"""
    return np.array([list(line) for line in s.strip().split("\n")])


def find_i_j_list(A: np.ndarray, target: str) -> list[tuple[int]]:
    """Returns all (i, j) such that A[i, j] = target"""
    return [(int(t[0]), int(t[1])) for t in zip(*np.where(A == target))]


def spread(A: np.ndarray, locs: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Spread the set of locations to neighboring non-wall locations"""
    locs_new = set()
    for i, j in locs:
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            _i, _j = i + di, j + dj
            if A[_i, _j] != "#":
                locs_new.add((_i, _j))
    return locs_new


def get_distances(A: np.ndarray) -> dict[tuple[int, int], int]:
    """For each non-wall location in A, find its distance to E
    This is just Dijkstra
    """
    iE, jE = find_i_j_list(A, "E")[0]
    distances = defaultdict(lambda: np.inf)
    distances[(iE, jE)] = 0
    covered = {(iE, jE)}
    frontier = [(iE, jE)]
    d = 0
    while frontier:
        frontier = spread(A, frontier)
        frontier = frontier - covered
        d += 1
        for i, j in frontier:
            distances[(i, j)] = min(distances[(i, j)], d)
        covered.update(frontier)
    return dict(distances)


def get_cheats(
    distances: dict[tuple[int, int], int],
    cheat_moves: list[tuple[int, int]],
) -> dict[tuple[int, int], int]:
    """Get the dictionary mapping each possible cheat to the time save it achieves
    Only allowed to use cheats in the moves provided
    Only return cheats that actually save time
    Keys are (i1, j1, i2, j2) for the cheat that goes from (i1, j1) to (i2, j2)
    """
    cheats = {}
    for i, j in distances.keys():
        for di, dj in cheat_moves:
            _i, _j = i + di, j + dj
            if (_i, _j) in distances.keys():
                time_save = distances[(i, j)] - distances[(_i, _j)] - abs(di) - abs(dj)
                if time_save > 0:
                    cheats[(i, j, _i, _j)] = time_save
    return cheats


def get_cheat_moves(r: int) -> list[tuple[int, int]]:
    """Return the possible cheat moves of a given radius"""
    cheat_moves = []
    for di in range(-r, r + 1):
        for dj in range(-r, r + 1):
            _r = abs(di) + abs(dj)
            if _r <= r:
                cheat_moves.append((di, dj))
    return cheat_moves


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse input into a numpy array
    A = parse_array(s)

    # get the dictionary matching each (i, j) to its distance to E
    distances = get_distances(A)

    # figure out all possible cheats within our 2 picosecond radius
    cheat_moves = get_cheat_moves(2)

    # iterate over (i, j) and possible cheats to see how much time save each one gives
    # get the dict mapping cheats to their time saves
    # only "keep" cheats that save a positive amount of time
    cheats = get_cheats(distances, cheat_moves)

    # count how many cheats save at least 100 picoseconds
    num_cheats = int((pd.Series(cheats) >= 100).sum())

    return num_cheats


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    A = parse_array(s)
    distances = get_distances(A)
    cheat_moves = get_cheat_moves(20)
    cheats = get_cheats(distances, cheat_moves)
    num_cheats = int((pd.Series(cheats) >= 100).sum())
    return num_cheats


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
