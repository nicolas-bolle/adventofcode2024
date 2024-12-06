"""Day 6
Uses Lab class to manage the lab + guard + the steps they take

Part 2 solution takes about 1 minutes
Maybe it's slow because I'm copying A_base every time and also python is slow?
Since I did the main optimization of not checking irrelevant obstacle locations
"""


# pylint: disable=unused-import, invalid-name, redefined-outer-name

from abc import ABC, abstractmethod
from functools import lru_cache

import re
from collections import deque
from frozendict import frozendict
import numpy as np
import pandas as pd

from utils.inputs import (
    get_input,
    split,
    split_newline,
    split_lax,
    list_map,
    list_reshape,
    get_int,
    get_float,
)

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

    MARKER_EMPTY = "."
    MARKER_VISITED = "X"
    MARKER_WALL = "#"

    guard_location = (None, None)
    guard_direction = ""

    exited = False
    looped = False
    history = set()

    def __init__(self, A):
        self.A = A
        self.n, self.m = A.shape
        self.guard_location, self.guard_direction = self.find_guard()
        self.exited = False
        self.history = {(self.guard_location, str(self.guard_direction))}
        self.looped = False

    def __str__(self):
        return "\n".join(["".join(row) for row in self.A])

    def find_guard(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.A[i, j] in self.DIRECTIONS.keys():
                    return (i, j), self.A[i, j]
        raise Exception("Guard not found")

    def step(self) -> str:
        """Take a single step, marking it and updating our self.history, self.exited, self.looped"""
        assert not self.exited, "Guard left the lab"

        # try a forward step
        direction_vector = self.DIRECTIONS[self.guard_direction]
        i = self.guard_location[0] + direction_vector[0]
        j = self.guard_location[1] + direction_vector[1]

        # abort if the guard stepped out of bounds
        try:
            assert i >= 0
            assert j >= 0
            assert i < self.n
            assert j < self.m
            stepping_onto = self.A[i, j]
        except:
            self.A[self.guard_location] = self.MARKER_VISITED
            self.guard_location = (None, None)
            self.guard_direction = ""
            self.exited = True
            return

        assert stepping_onto in (
            self.MARKER_EMPTY,
            self.MARKER_VISITED,
            self.MARKER_WALL,
        ), f"Unrecognized marker {stepping_onto}"

        if not self.A[i, j] == self.MARKER_WALL:
            # forward step worked
            self.A[self.guard_location] = self.MARKER_VISITED
            self.guard_location = (i, j)
            self.A[self.guard_location] = self.guard_direction
            key = ((i, j), str(self.guard_direction))
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

    def count_guard_locs_visited(self):
        return int((self.A == self.MARKER_VISITED).sum())


def solution_part1(s: str):
    """Part 1 solution from the plaintext input"""
    A = np.array(list(map(list, s.strip().split("\n"))))
    lab = Lab(A)
    lab.step_until_exit()
    c = lab.count_guard_locs_visited()
    return c


def solution_part2(s: str):
    """Part 2 solution from the plaintext input"""
    # first have the guard explore the lab, since it's only worth placing obstacles where they walk
    A_base = np.array(list(map(list, s.strip().split("\n"))))
    A = A_base.copy()
    lab_base = Lab(A)
    lab_base.step_until_exit()
    n, m = A_base.shape

    c = 0
    # iterate over places we could put this new obstacle, and check if they give a guard loop
    for i in range(n):
        for j in range(m):
            # we can only place a new obstacle where there's space
            # and its only worth checking locations that the guard's "base path" would cross
            if A_base[i, j] == "." and lab_base.A[i, j] == "X":
                A = A_base.copy()
                A[i, j] = "#"
                lab = Lab(A)
                has_loop = lab.check_if_loop()
                if has_loop:
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
