"""Day 21

Runs in milliseconds

This took a LOT of thinking for part 1
Then part 2 was an easy generalization with set_up_robots()

Here's how I thought about things:
- A 'cycle' is a sequence of key presses starting from 'A' and ending with 'A'
    - Ex. '123A', or '<>^A'
    - Cycles work independently of each other, since you always reset to being "at" location 'A'
- Each keyboard is a "layer"
    - We stack layers
    - Start with the numpad layer
    - Then arrow key layers
- On a given layer, given a cycle you can ask what's the minimum number of key presses to achieve the cycle
    - This is calc_min_num_presses_for_cycle()
    - This can be cached
        - (Assuming the setup of layers stays the same)
        - This is pretty useless for the numpad layer
        - But it's insanely useful for the arrow key layers, since they'll be repeating the same cycles over and over
    - If a layer has no layer above it, the number of presses is just the length of the cycle
        - Ex. '123A' is just 4 button presses
    - If there are layers above it, things get more complex
- A 'segment' is each successive button press in a cycle
    - Ex. '123A' has 3 segments: A -> 1, 1 -> 2, 2 -> 3, 3 -> A
    - **Each segment is a cycle in the layer above!**
    - That means the segments can be treated independently!
    - The tricky bit is that there are multiple cycles that achieve the same segment
        - Ex. A -> 2 can be achieved by '<^A' or '^<A', and also things like '^^<vA'
    - You can show you only need to consider minimum length cycles
        - Ex. for A -> 2 you just need to consider '<^A' and '^<A'
    - Finding the cycles that achieve a segment can be cached
- So here's the eval process:
    - Call calc_min_num_presses_for_cycle() on the lowest layer
    - For each segment, find all shortest length cycles (in the layer above) that achieve it
    - Iterate through those cycles on the layer above, running calc_min_num_presses_for_cycle() on each (with the layer above)
    - Pick the smallest one (for this segment), and then move on to the next segment
    - Add up the segments and that's the return
- Sidenote: if there's just one layer above, the calculation is a bit simpler
    - Ex. A -> 5 can be achieved in 4 presses by something like '^<^A'
    - But if there's another layer above, then '^<^A' is bad and '<^^A' is better
        - Because it has repeated key presses, which means we don't have to move around as much

For implementation, I implemented the arrow keys (ArrowKeys) with the numpad a subclass (NumKeys)
calc_min_num_presses_for_cycle() for the recursive key presses calc (with caching)
cycles_for_segment() for finding the cycles that achieve a segment (with caching)
"""

# pylint: disable=invalid-name, redefined-outer-name

from typing import Self
from functools import cache
import numpy as np

from utils.inputs import get_input

DAY = 21


class ArrowKeys:
    """Represents the <>^vA keys
    A "cycle" is a sequence of keypresses starting from A and ending with A
    It's made up of "segments" which are each just a cycle in the layer above (if it exists)
    """

    # the layer above this one
    next_layer: Self = None

    # keys that can be pressed
    KEYS = {
        "A": (0, 0),
        "<": (-2, -1),
        "v": (-1, -1),
        "^": (-1, 0),
        ">": (0, -1),
    }

    # the effect of pressing each arrow key
    VECTS = {
        "<": (-1, 0),
        "v": (0, -1),
        "^": (0, 1),
        ">": (1, 0),
    }

    # locations of keys
    KEY_LOCS = set()

    def __init__(self):
        assert "A" in self.KEYS
        assert self.KEYS["A"] == (0, 0)

        # locations of keys
        self.KEYS_LOCS = set(self.KEYS.values())

    @cache
    def calc_min_num_presses_for_cycle(self, cycle: str) -> int:
        """Return the number of presses needed for the given cycle"""
        # basic check
        assert cycle[-1] == "A"

        # if there's no layer above us, the number of presses is just the length of the cycle
        if self.next_layer is None:
            return len(cycle)

        # otherwise either 1 or 2 layers are above us
        # those behave differently, but can both be handled by the 2 layer logic
        num_presses_cycle = 0

        # start at 'A'
        i1, j1 = 0, 0

        # iterate through the button presses (segments)
        for button in cycle:
            # the minimum number of presses for this segment
            num_presses_segment = np.inf

            # the location we move to
            i2, j2 = self.KEYS[button]

            # find all the ways of achieving this segment as a sequence of key presses
            _cycles = self.cycles_for_segment(i1, j1, i2, j2)

            # check how many presses each of those takes
            for _cycle in _cycles:
                _num_presses = self.next_layer.calc_min_num_presses_for_cycle(_cycle)
                num_presses_segment = min(num_presses_segment, _num_presses)

            # update the min number of presses for this cycle
            num_presses_cycle += num_presses_segment

            # update our location after this segment
            i1, j1 = i2, j2

        return num_presses_cycle

    @cache
    def cycles_for_segment(self, i1, j1, i2, j2) -> list[str]:
        """Returns a list of the minimum length cycles achieving the segment (i1, j1) -> (i2, j2)
        Makes sure we never leave the number pad
        Caching to avoid constantly recalculating these (esp for the arrow keys)
        """
        # the vector we want to achieve
        di, dj = i2 - i1, j2 - j1

        # base case
        if di == 0 and dj == 0:
            return "A"

        # otherwise, work recursively
        cycles = []

        # try each of the key presses that can be done
        for key, (_di, _dj) in self.VECTS.items():
            # if the key press takes us in the right direction, that's a good start
            # using a dot product here
            if di * _di + dj * _dj > 0:
                # this is the location the key press would take us to
                _i1 = i1 + _di
                _j1 = j1 + _dj

                # check that the key press would keep us on our grid
                if (_i1, _j1) in self.KEYS_LOCS:
                    # if you reached here, the key press both helps us and keeps us on our grid; nice!

                    # after doing that key press, recursive call
                    _cycles = self.cycles_for_segment(_i1, _j1, i2, j2)
                    _cycles = [key + _cycle for _cycle in _cycles]
                    cycles.extend(_cycles)

        return cycles


class NumKeys(ArrowKeys):
    """The num keys 0-9 grid"""

    KEYS = {
        "A": (0, 0),
        "0": (-1, 0),
        "1": (-2, 1),
        "2": (-1, 1),
        "3": (0, 1),
        "4": (-2, 2),
        "5": (-1, 2),
        "6": (0, 2),
        "7": (-2, 3),
        "8": (-1, 3),
        "9": (0, 3),
    }


def set_up_robots(num_middle_men: int) -> NumKeys:
    """Set up key pad robots with the given number of middle men
    So the num pad, middle men, and then the user arrow pad
    """
    robot = NumKeys()
    _robot = robot
    for _ in range(num_middle_men + 1):
        _robot.next_layer = ArrowKeys()
        _robot = _robot.next_layer
    return robot


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse input into the cycles we want to achieve
    cycles = s.strip().split()

    # set up the robots that'll be doing the key presses
    robot = set_up_robots(num_middle_men=2)

    # for each cycle, extract its number
    cycles_nums = [int(cycle[:-1]) for cycle in cycles]

    # for each cycle, calculate the minimum number of presses needed
    cycles_num_presses = []
    for cycle in cycles:
        cycles_num_presses.append(robot.calc_min_num_presses_for_cycle(cycle))

    # calculate the complexity
    complexity = int(sum(np.array(cycles_num_presses) * np.array(cycles_nums)))

    return complexity


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    cycles = s.strip().split()
    robot = set_up_robots(num_middle_men=25)
    cycles_nums = [int(cycle[:-1]) for cycle in cycles]
    cycles_num_presses = []
    for cycle in cycles:
        cycles_num_presses.append(robot.calc_min_num_presses_for_cycle(cycle))
    complexity = int(sum(np.array(cycles_num_presses) * np.array(cycles_nums)))
    return complexity


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
