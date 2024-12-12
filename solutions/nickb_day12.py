"""Day 12"""

# pylint: disable=invalid-name, redefined-outer-name

from collections import defaultdict
import numpy as np

from utils.inputs import get_input

DAY = 12


def spread(A: np.ndarray, locs: set) -> set:
    """Get the set of locs we spread to in 1 step"""
    n, m = A.shape

    # get the region
    i, j = next(iter(locs))
    r = A[i, j]

    new_locs = set()
    for i, j in locs:
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            _i, _j = i + di, j + dj

            # check bounds
            if not (0 <= _i < n and 0 <= _j < m):
                continue

            # check region
            if A[_i, _j] != r:
                continue

            # add loc
            new_locs.add((_i, _j))

    return new_locs


def find_region(A: np.ndarray, i: int, j: int) -> set:
    """Find the set of locations for the region of A[i, j]
    Does spreading just on the "frontier" to make things a bit quicker
    """
    locs = {(i, j)}
    frontier = {(i, j)}
    n = len(locs) + 1
    while len(locs) != n:
        n = len(locs)
        new_locs = spread(A, frontier)
        frontier = new_locs - locs
        locs = locs | frontier
    return locs


def find_regions(A: np.ndarray) -> list[set]:
    """Return the list of locs sets of regions"""
    # set of points with regions already assigned
    assigned = set()

    regions = []

    n, m = A.shape
    for i in range(n):
        for j in range(m):
            if (i, j) in assigned:
                continue
            region = find_region(A, i, j)
            regions.append(region)
            assigned.update(region)

    return regions


def get_region_area(region: set):
    """Area of a region"""
    return len(region)


def get_region_perimeter(region: set):
    """Perimeter of a region"""
    perimeter = 0
    for i, j in iter(region):
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            _i, _j = i + di, j + dj
            if (_i, _j) not in region:
                perimeter += 1
    return perimeter


def get_region_num_sides(region: set):
    """Number of sides of a region"""
    # the perimeter segements, represented as loc + direction the side was found in
    # organized by the direction, since for finding sides we can treat each separately
    perimeter_locs_by_dir = defaultdict(list)
    for i, j in iter(region):
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            _i, _j = i + di, j + dj
            if (_i, _j) not in region:
                direction = (di, dj)
                location = (i, j)
                perimeter_locs_by_dir[direction].append(location)

    # for each direction, join together adjacent locations to get the sides
    # get_num_vertical_sides() does this, we just need to pass it locations for "veritical edges"
    sides = 0
    for direction, locs in perimeter_locs_by_dir.items():
        # if the edge was found in an x direction, flips the tuples for get_num_horizontal_sides()
        if direction[0]:
            _locs = [(j, i) for i, j in locs]
        else:
            _locs = locs
        _sides = get_num_horizontal_sides(_locs)
        sides += _sides

    return sides


def get_num_horizontal_sides(locs: list):
    """Given a list of tuples (i, j) representing locations that have sides in the up (or down) direction,
        return the number of joined sides
    We can do this by treating each j level separately, and looking for connected components in the i direction
    """
    levels = defaultdict(list)
    for i, j in locs:
        levels[j].append(i)

    sides = 0
    for level in levels.values():
        # sneaky, but the number of distinct components is the number of gaps between sides +1
        level = sorted(level)
        _sides = sum(np.diff(np.array(level)) > 1) + 1
        sides += _sides

    return int(sides)


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    A = np.array([list(line) for line in s.strip().split("\n")])
    regions = find_regions(A)
    areas = [get_region_area(region) for region in regions]
    perimeters = [get_region_perimeter(region) for region in regions]
    return int(sum(np.array(areas) * np.array(perimeters)))


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    A = np.array([list(line) for line in s.strip().split("\n")])
    regions = find_regions(A)
    areas = [get_region_area(region) for region in regions]
    num_sides = [get_region_num_sides(region) for region in regions]
    return int(sum(np.array(areas) * np.array(num_sides)))


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
