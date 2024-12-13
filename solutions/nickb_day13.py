"""Day 13

Define the vectors v_a, v_b, v_g for the x, y movement associated to the button presses and goal
If v_a and v_b are linearly independent:
- The right number of A and B presses will be unique
- It can be found by solving a linear system of equations and checking the solution works

It turns out the v_a and v_b are linearly independent (verified in an assert below)
And numpy.linalg.solve turns out to be numerically precise enough for us
"""

# pylint: disable=invalid-name, redefined-outer-name

import re
import math
import numpy as np

from utils.inputs import get_input

DAY = 13

REGEX = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"

PRESSES_LIMIT_PART1 = 100

OFFSET_PART2 = 10000000000000


def parse_game_part1(block):
    """Parse the 3 lines corresponding to a game for part 1"""
    ax, ay, bx, by, gx, gy = _parse_game(block)
    return ax, ay, bx, by, gx, gy


def parse_game_part2(block):
    """Parse the 3 lines corresponding to a game for part 2"""
    ax, ay, bx, by, gx, gy = _parse_game(block)
    return ax, ay, bx, by, gx + OFFSET_PART2, gy + OFFSET_PART2


def _parse_game(block):
    """Helper for the basic parsing"""
    # extract the numbers
    res = re.match(REGEX, block.strip())
    assert res is not None
    nums = [int(x) for x in res.groups()]
    assert len(nums) == 6
    ax, ay, bx, by, gx, gy = tuple(nums)

    # linear independence check using gcd to "reduce" the vectors
    # I just wanted to avoid any numerical issues for this
    d = math.gcd(ax, ay, bx, by)
    _ax, _ay, _bx, _by = ax // d, ay // d, bx // d, by // d
    assert not (_ax == _ay and _bx == _by)

    return ax, ay, bx, by, gx, gy


def get_a_b_for_game(game: tuple) -> tuple[int | None, int | None]:
    """Get the number of A and B presses needed to solve a game
    Or None if it's not possible
    """
    # unpack
    assert len(game) == 6
    ax, ay, bx, by, gx, gy = game

    # linear algebra to the rescue
    A = np.array([[ax, bx], [ay, by]])
    v = np.array([[gx], [gy]])
    x = np.linalg.solve(A, v)
    a, b = tuple(x.reshape(-1))

    # round, check, return
    a = int(np.round(a))
    b = int(np.round(b))
    if ax * a + bx * b == gx and ay * a + by * b == gy:
        return a, b
    return None, None


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse games as tuples ax, ay, bx, by, gx, gy giving the vectors v_a, v_b, v_g
    games = [parse_game_part1(block) for block in s.strip().split("\n\n")]

    # solve the games and count up the tokens
    tokens = 0
    for game in games:
        a, b = get_a_b_for_game(game)
        if (
            a is not None
            and b is not None
            and a <= PRESSES_LIMIT_PART1
            and b <= PRESSES_LIMIT_PART1
        ):
            tokens += 3 * a + b

    return tokens


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    games = [parse_game_part2(block) for block in s.strip().split("\n\n")]

    tokens = 0
    for game in games:
        a, b = get_a_b_for_game(game)
        if a is not None and b is not None:
            tokens += 3 * a + b

    return tokens


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
