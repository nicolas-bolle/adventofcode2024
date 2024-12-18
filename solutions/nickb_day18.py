"""Day 18

At first I did part 2 with a manual binary search
Then I automated the binary search like it is below
scipy is a bit overkill, but it was the quickest for me to set up
"""

# pylint: disable=invalid-name, redefined-outer-name

import numpy as np
from scipy.optimize import bisect

from utils.inputs import get_input

DAY = 18


def spread(
    locs: set[tuple[int, int]],
    n: int,
    corrupted: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    """Spread the set of locations on a grid with x/y coords 0, ..., n
    Avoid the locations in 'corrupted'
    Modifies the variable 'locs' (i.e. in place)
    """
    new_locs = set()
    for i, j in locs:
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            _i, _j = i + di, j + dj
            if (0 <= _i <= n) and (0 <= _j <= n):
                new_locs.add((i + di, j + dj))
    locs = (locs | new_locs) - corrupted
    return locs


def check_possible(
    all_corrupted: list[tuple[int, int]],
    num_corrupted: int,
    n: int,
) -> bool:
    """Check if it's possible to reach (n, n) from (0, 0) with the given number of corrupted bits"""
    corrupted = set(all_corrupted[:num_corrupted])

    locs = {(0, 0)}
    for _ in range(n * n):
        len_locs = len(locs)
        locs = spread(locs, n, corrupted)

        # success if we find the exit
        if (n, n) in locs:
            return True

        # stop iterating if we've explored everything we can
        if len(locs) == len_locs:
            break

    return False


def bisect_wrapper(x, all_corrupted, n):
    """Wrapper for check_possible so it can be used with scipy.optimize.bisect"""
    if check_possible(all_corrupted, int(x), n):
        return 1
    return -1


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse into into a list of tuples (i, j) of the bits that'll get corrupted
    all_corrupted = [
        (int(t[0]), int(t[1]))
        for t in np.array(s.strip().replace(",", " ").split()).reshape(-1, 2)
    ]

    # hardcoded inputs
    n = 70
    num_corrupted = 1024

    # iterate to reach the exit
    corrupted = set(all_corrupted[:num_corrupted])
    locs = {(0, 0)}
    num_steps = 0
    while (n, n) not in locs:
        num_steps += 1
        locs = spread(locs, n, corrupted)

    return num_steps


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    all_corrupted = [
        (int(t[0]), int(t[1]))
        for t in np.array(s.strip().replace(",", " ").split()).reshape(-1, 2)
    ]
    n = 70

    # scipy to handle the bisection search for the fatal number of corruptions
    root = bisect(
        bisect_wrapper, 1024, len(all_corrupted), args=(all_corrupted, n), xtol=0.2
    )
    num_of_fatal_corruption = int(np.round(root))
    print(num_of_fatal_corruption)

    # the fatal corruption tuple
    fatal_tuple = all_corrupted[num_of_fatal_corruption - 1]

    # format answer
    assert len(fatal_tuple) == 2
    fatal_str = f"{fatal_tuple[0]},{fatal_tuple[1]}"

    return fatal_str


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
