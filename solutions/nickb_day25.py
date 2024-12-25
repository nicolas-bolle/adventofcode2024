"""Day 25

Nothing fancy, just iterate over locks and keys to see if they fit
"""

# pylint: disable=invalid-name, redefined-outer-name

import numpy as np

from utils.inputs import get_input


DAY = 25


def parse_input(s: str) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Parse input into lists of locks and keys (as np arrays)
    Includes a few checks that things look as expected
    """
    locks = []
    keys = []
    blocks = s.strip().split("\n\n")

    A = parse_block(blocks[0])
    n, m = A.shape

    for block in blocks:
        A = parse_block(block)
        assert A.shape == (n, m)
        top_row = A[0, :]
        bottom_row = A[-1, :]
        is_lock = all(top_row == "#")
        is_key = all(bottom_row == "#")
        assert is_lock ^ is_key
        if is_lock:
            locks.append(A)
        else:
            keys.append(A)

    return locks, keys


def parse_block(block: str) -> np.ndarray:
    """Parse a string into a np array"""
    A = np.array([list(line) for line in block.split("\n")])
    return A


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse input into lists of locks and keys
    locks, keys = parse_input(s)

    # nothing fancy, just iterate over locks and keys to see if they fit
    num_fit = 0
    for lock in locks:
        for key in keys:
            overlap = (lock == "#") & (lock == key)
            if not overlap.any():
                num_fit += 1

    return num_fit


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    # dummy solution
    return 0


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
