"""Day 4"""


# pylint: disable=invalid-name, redefined-outer-name

import numpy as np

from utils.inputs import get_input

DAY = 4


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input
    I manually coded in the 8 relative positions (horizontal, vertical, diagonal) that an 'XMAS' could appear in
    The code (inefficiently) loops through all shifts of these to look for 'XMAS'es
    """
    A = np.array([list(line) for line in s.strip().split("\n")])

    c = 0

    idxs = [
        ([0, 0, 0, 0], [0, 1, 2, 3]),
        ([0, 0, 0, 0], [0, -1, -2, -3]),
        ([0, 1, 2, 3], [0, 0, 0, 0]),
        ([0, -1, -2, -3], [0, 0, 0, 0]),
        ([0, 1, 2, 3], [0, 1, 2, 3]),
        ([0, 1, 2, 3], [0, -1, -2, -3]),
        ([0, -1, -2, -3], [0, 1, 2, 3]),
        ([0, -1, -2, -3], [0, -1, -2, -3]),
    ]

    padding = 5
    n = len(A)
    for idx_x, idx_y in idxs:
        for offset_x in range(-padding, n + padding + 1):
            for offset_y in range(-padding, n + padding + 1):
                _idx_x = np.array(idx_x) + offset_x
                _idx_y = np.array(idx_y) + offset_y

                if (
                    min(_idx_x) < 0
                    or min(_idx_y) < 0
                    or max(_idx_x) >= n
                    or max(_idx_y) >= n
                ):
                    continue

                text = "".join(A[_idx_x, _idx_y])
                if text == "XMAS":
                    c = c + 1

    return c


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input
    For this part we just need one "pattern", and we can match it to 4 'X-MAS'es
    The 4 correspond to the 4 rotations of the X
    """
    A = np.array([list(line) for line in s.strip().split("\n")])

    c = 0

    padding = 4
    n = len(A)

    idx_x = [0, -1, -1, 1, 1]
    idx_y = [0, -1, 1, 1, -1]

    matches = [
        "AMMSS",
        "AMSSM",
        "ASSMM",
        "ASMMS",
    ]

    for offset_x in range(-padding, n + padding + 1):
        for offset_y in range(-padding, n + padding + 1):
            _idx_x = np.array(idx_x) + offset_x
            _idx_y = np.array(idx_y) + offset_y

            if (
                min(_idx_x) < 0
                or min(_idx_y) < 0
                or max(_idx_x) >= n
                or max(_idx_y) >= n
            ):
                continue

            text = "".join(A[_idx_x, _idx_y])
            if text in matches:
                c = c + 1

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
