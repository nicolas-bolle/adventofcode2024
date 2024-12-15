"""Day 15

I really liked part 2
The functions check_move() and make_move() do most of the work

At first for part 1 I had a function attempt_move() which was basically check_move() + make_move()
But for part 2 I needed to split those thins out separately
Another important thing for part 2 was that when you move one half
    of a double box vertically you need to move the other half
But making sure to avoid infinite recursion when doing that
"""

# pylint: disable=invalid-name, redefined-outer-name

import numpy as np

from utils.inputs import get_input

DAY = 15

# translating characters to vectors
DICT_MOVE_TO_VEC = {
    "^": (-1, 0),
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
}


def parse_input_part1(s: str) -> tuple[np.ndarray, list[str]]:
    """Parse into an array A and list of move characters (for part 1)"""
    s1, s2 = tuple(s.split("\n\n"))
    A = np.array([list(line) for line in s1.split("\n")])
    moves = list(s2.replace("\n", ""))
    return A, moves


def parse_input_part2(s: str) -> tuple[np.ndarray, list[str]]:
    """Parse into an array A and list of move characters (for part 2)"""
    s1, s2 = tuple(s.split("\n\n"))
    A = np.array(
        [
            list(
                line.replace("#", "##")
                .replace("O", "[]")
                .replace(".", "..")
                .replace("@", "@.")
            )
            for line in s1.split("\n")
        ]
    )
    moves = list(s2.replace("\n", ""))
    return A, moves


def check_move(A: np.ndarray, i: int, j: int, di: int, dj: int) -> bool:
    """Check if we can move A[i, j] by (di, dj)"""
    assert (di, dj) in ((0, 1), (0, -1), (1, 0), (-1, 0))

    # if we're moving nothing, then we're trivially successful
    if A[i, j] == ".":
        return True

    # if we're moving a wall, we fail
    if A[i, j] == "#":
        return False

    # otherwise we're moving the player or a box
    # so we need to see if the move in front of us would succeed

    # player
    if A[i, j] == "@":
        return check_move(A, i + di, j + dj, di, dj)

    # single width box
    if A[i, j] == "O":
        return check_move(A, i + di, j + dj, di, dj)

    # double width box from the side
    if A[i, j] in ("[", "]") and di == 0:
        return check_move(A, i + di, j + dj, di, dj)

    # double width box vertically, pushing the left side of it
    if A[i, j] == "[" and dj == 0:
        return check_move(A, i + di, j + dj, di, dj) and check_move(
            A, i + di, j + dj + 1, di, dj
        )

    # double width box vertically, pushing the right side of it
    if A[i, j] == "]" and dj == 0:
        return check_move(A, i + di, j + dj - 1, di, dj) and check_move(
            A, i + di, j + dj, di, dj
        )

    # unhandled case
    raise Exception("Unhandled case!")


def make_move(
    A: np.ndarray, i: int, j: int, di: int, dj: int, double_box_push: bool = True
) -> tuple[int, int]:
    """Move A[i, j] by (di, dj), returning the coords moved to
    double_box_push = True means if we're moving one half of a double box we should also move the other half
    So use double_box_push = False when you initiate the move of that other half
    """
    assert (di, dj) in ((0, 1), (0, -1), (1, 0), (-1, 0))

    # moving nothing
    if A[i, j] == ".":
        return di, dj

    # moving a wall
    if A[i, j] == "#":
        raise Exception("Unable to move a wall")

    # do the recursive moves
    did_recursive = False

    # player
    if A[i, j] == "@":
        did_recursive = True
        make_move(A, i + di, j + dj, di, dj)

    # single width box
    if A[i, j] == "O":
        did_recursive = True
        make_move(A, i + di, j + dj, di, dj)

    # double width box from the side
    if A[i, j] in ("[", "]") and di == 0:
        did_recursive = True
        make_move(A, i + di, j + dj, di, dj)

    # double width box vertically, pushing the left side of it
    if A[i, j] == "[" and dj == 0:
        did_recursive = True
        make_move(A, i + di, j + dj, di, dj)
        make_move(A, i + di, j + dj + 1, di, dj)
        if double_box_push:
            # initiate a move of the other half of the box
            make_move(A, i, j + 1, di, dj, double_box_push=False)

    # double width box vertically, pushing the right side of it
    if A[i, j] == "]" and dj == 0:
        did_recursive = True
        make_move(A, i + di, j + dj - 1, di, dj)
        make_move(A, i + di, j + dj, di, dj)
        if double_box_push:
            # initiate a move of the other half of the box
            make_move(A, i, j - 1, di, dj, double_box_push=False)

    # unhandled case
    if not did_recursive:
        raise Exception("Unhandled case!")

    # and finally move ourselves
    A[i + di, j + dj] = A[i, j]
    A[i, j] = "."

    return i + di, j + dj


def find_robot(A: np.ndarray) -> tuple[int]:
    """Returns (i, j) such that A[i, j] = '@'"""
    return (int(t) for t in next(zip(*np.where(A == "@"))))


def get_box_gps_coords(A: np.ndarray) -> list[int]:
    """Return the list of GPS coords (ints)
    Works for both part 1 and part 2
    """
    I, J = np.where((A == "O") | (A == "["))
    return [int(t) for t in 100 * I + J]


def array_to_string(A: np.ndarray) -> str:
    """Util so that print(array_to_string(A)) prints an array A nicely"""
    return "\n".join(["".join(line) for line in A])


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse input
    A, moves = parse_input_part1(s)

    # i, j will keep track of the location of the robot
    i, j = find_robot(A)

    # attempt each move
    for move in moves:
        move_tuple = A, i, j, *DICT_MOVE_TO_VEC[move]

        # first check if its possible
        if check_move(*move_tuple):
            # if it is possible, do it
            i, j = make_move(*move_tuple)

    # return the sum of the gps coords
    return sum(get_box_gps_coords(A))


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    A, moves = parse_input_part2(s)
    i, j = find_robot(A)
    for move in moves:
        move_tuple = A, i, j, *DICT_MOVE_TO_VEC[move]
        if check_move(*move_tuple):
            i, j = make_move(*move_tuple)
    return sum(get_box_gps_coords(A))


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
