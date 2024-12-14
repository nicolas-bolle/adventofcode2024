"""Day 14

I don't like part 2
See solution_part2() for a sketch of how I solved part 2,
    but basically it was me manually scanning through
    nearly 8000 print outs to look for a Christmas tree
You could narrow the search by devising some Christmas tree heuristic,
    like the standard deviation one I wrote after the fact
But since I didn't know what this tree would look like,
    the manual approach seemed more reliable
Plus the heuristic idea feels too "hope" based
"""

# pylint: disable=invalid-name, redefined-outer-name

import re
from collections import defaultdict
import numpy as np

from utils.inputs import get_input

DAY = 14

# x width and y width of the space
WX, WY = 101, 103


def step_robot(px, py, vx, vy, wx, wy):
    """Move a robot forward one time step"""
    return (px + vx) % wx, (py + vy) % wy


def step_robots(robots, wx, wy):
    """Move all robots forward one time step"""
    for i in range(len(robots)):
        px, py, vx, vy = robots[i]
        px, py = step_robot(px, py, vx, vy, wx, wy)
        robots[i] = (px, py, vx, vy)
    return robots


def robots_to_string(robots, wx, wy):
    """Return a string representing the space visually"""
    A = np.full((wx, wy), ".")
    for px, py, _, _ in robots:
        A[px, py] = "#"
    A = A.transpose()
    print("\n".join(["".join(line) for line in A]))


def assign_sector(px, py, wx, wy):
    """Assign a "sector" (i, j) to the robot location (px, py),
    where i, j are one of -1, 0, or 1
    """
    return int(np.sign(px - wx // 2)), int(np.sign(py - wy // 2))


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse robots into tuples (px, py, vx, vy)
    robots = [
        tuple(int(n) for n in re.findall(r"-?\d+", line)) for line in s.split("\n")
    ]

    # run 100 steps
    for _ in range(100):
        robots = step_robots(robots, WX, WY)

    # assign sectors to all the robots, counting up the number in each sector
    sector_counts = defaultdict(int)
    for px, py, _, _ in robots:
        sector = assign_sector(px, py, WX, WY)
        sector_counts[sector] += 1

    # calculate the safety factor using the relevant sectors
    safety_factor = 1
    for sector, ct in sector_counts.items():
        if abs(sector[0]) == 1 and abs(sector[1]) == 1:
            safety_factor *= ct

    return safety_factor


def solution_part2(s: str, print_verification=False) -> int:
    """Part 2 solution from the plaintext input
    Using print_verification=True will print the Christmas tree Easter egg

    The first commented portion is what I manually ran a total of 8 times,
        each time manually scanning through the 1000 print outs in
        VSCode text viewer to look for the Christmas tree
    An important fact is that the images will loop after WX * WY steps,
        so worst case I'd have had to scan through *only* 11_000 print outs

    The second commented portion is something I made after the fact:
        since standard deviations are typically 30, a threshold of 25
        easily detects the Christmas tree
    """

    if print_verification:
        robots = [
            tuple(int(n) for n in re.findall(r"-?\d+", line)) for line in s.split("\n")
        ]

        for _ in range(7916):
            robots = step_robots(robots, WX, WY)
        print(robots_to_string(robots, WX, WY))

    # for i in range(1000):
    #    print(i)
    #    print(robots_to_string(robots, WX, WY))
    #    robots = step_robots(robots, WX, WY)
    #    print("-" * 100)

    # for i in range(WX * WY):
    #    x = [px for px, _, _, _ in robots]
    #    y = [py for _, py, _, _ in robots]
    #    if np.std(x) < 25 or np.std(y) < 25:
    #        print(i)
    #        print(robots_to_string(robots, WX, WY))
    #    robots = step_robots(robots, WX, WY)

    return 7916


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
