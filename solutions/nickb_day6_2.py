"""Day 6

Takes 15 seconds
Faster that my other solution since it works with sets of locations instead of the entire lab
"""

# pylint: disable=invalid-name, redefined-outer-name

import numpy as np

from utils.inputs import get_input

DAY = 6


class Lab:
    """Represents a lab with a guard in it
    Manages having the guard take steps
    """

    DIRECTIONS = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }
    ROTATIONS = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^",
    }

    min_i = None
    max_i = None
    min_j = None
    max_j = None

    wall_locs = set()

    guard_location = (None, None)
    guard_direction = ""

    exited = False
    looped = False
    history = set()

    def __init__(
        self, min_i, max_i, min_j, max_j, wall_locs, guard_location, guard_direction
    ):
        self.min_i = min_i
        self.max_i = max_i
        self.min_j = min_j
        self.max_j = max_j

        self.wall_locs = wall_locs

        self.guard_location = guard_location
        self.guard_direction = guard_direction

        self.exited = False
        self.looped = False
        self.history = {(self.guard_location, self.guard_direction)}

    def step(self) -> str:
        """Take a single step, marking it and updating our self.history, self.exited, self.looped"""
        assert not self.exited, "Guard left the lab"

        # try a forward step
        direction_vector = self.DIRECTIONS[self.guard_direction]
        i = self.guard_location[0] + direction_vector[0]
        j = self.guard_location[1] + direction_vector[1]

        # abort if the guard stepped out of bounds
        try:
            assert i >= self.min_i
            assert j >= self.min_j
            assert i <= self.max_i
            assert j <= self.max_j
        except:  # pylint:disable=bare-except
            self.guard_location = (None, None)
            self.guard_direction = ""
            self.exited = True
            return

        if (i, j) not in self.wall_locs:
            # forward step worked
            self.guard_location = (i, j)
            key = (self.guard_location, self.guard_direction)
            self.looped = key in self.history
            self.history.add(key)
            return

        # otherwise, the guard rotates and tries again
        self.guard_direction = self.ROTATIONS[self.guard_direction]
        self.step()

    def step_until_exit(self):
        """Step until self.exited = True"""
        while True:
            self.step()
            if self.exited:
                return

    def check_if_loop(self):
        """Step until exit or loop
        If exit, return False
        If loop, return True
        """
        while True:
            self.step()
            if self.exited:
                return False
            if self.looped:
                return True

    @property
    def history_locs(self):
        """The set of locations in the history"""
        return {loc for loc, _ in self.history}

    @property
    def n_locs_visited(self):
        """How many distinct locations the guard visited"""
        return len(self.history_locs)


def parse_input(s):
    """Parse input into the things needed to make a Lab object"""
    A = np.array([list(line) for line in s.strip().split("\n")])

    min_i, min_j = 0, 0
    max_i, max_j = A.shape[0] - 1, A.shape[1] - 1

    wall_locs = set()
    guard_location = None
    guard_direction = None

    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            if A[i, j] == "#":
                wall_locs.add((i, j))
            if A[i, j] in ("^", ">", "v", "<"):
                assert guard_location is None
                guard_location = (i, j)
                guard_direction = str(A[i, j])

    assert guard_location is not None
    assert guard_direction is not None

    return min_i, max_i, min_j, max_j, wall_locs, guard_location, guard_direction


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    lab = Lab(*parse_input(s))
    lab.step_until_exit()
    return lab.n_locs_visited


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    # first have the guard explore the lab, since it's only worth placing obstacles where they walk
    min_i, max_i, min_j, max_j, wall_locs, guard_location, guard_direction = (
        parse_input(s)
    )

    # find the locations the "original" path passes through
    lab_base = Lab(
        min_i, max_i, min_j, max_j, wall_locs, guard_location, guard_direction
    )
    lab_base.step_until_exit()
    relevant_locs = lab_base.history_locs

    c = 0
    # see if placing obstacles at these relevant locs gives a guard loop
    for i, j in relevant_locs:
        assert (i, j) not in wall_locs

        # add the obstacle
        wall_locs.add((i, j))

        # check if we get a loop
        lab = Lab(
            min_i, max_i, min_j, max_j, wall_locs, guard_location, guard_direction
        )
        has_loop = lab.check_if_loop()
        if has_loop:
            c = c + 1

        # remove the obstacle
        wall_locs.remove((i, j))

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
