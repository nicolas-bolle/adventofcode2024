"""Day 9

Faster than my other solution and much easier to follow
I basically copied Marcos Huerta
https://github.com/KMX-Advent-of-Code/2024-Advent-of-Code/blob/main/Day9/Marcos_Day9.py
"""

# pylint: disable=invalid-name, redefined-outer-name

import numpy as np
from utils.inputs import get_input

DAY = 9


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # make the disk as a list, with -1 = gap
    disk = []
    k = 0
    files_bool = True
    for num in s:
        if files_bool:
            disk.extend([k] * int(num))
            k += 1
        else:
            disk.extend([-1] * int(num))
        files_bool = not files_bool
    disk = np.array(disk)

    # get indices of filled and gap locations
    (idx_filled,) = np.nonzero(disk >= 0)
    (idx_free,) = np.nonzero(disk == -1)

    # one by one, move the filled ones (from the end) into the gap locations
    for i, j in zip(idx_filled[::-1], idx_free):
        if i < j:
            break
        disk[j] = disk[i]
        disk[i] = -1

    # compute answer
    disk[disk == -1] = 0
    soln = int(sum(np.array(disk) * np.array(range(len(disk)))))

    return soln


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    # a block is a tuple (file_id, size)
    # make a list of blocks representing the disk
    disk_blocks = []
    k = 0
    i = 0
    files_bool = True
    for size in s:
        if files_bool:
            block = (k, int(size))
            k += 1

            # important fact!
            # since if there was a block with size zero then
            # we'd need to merge adjacent gaps in some places
            assert block[1]

        else:
            block = (None, int(size))

        disk_blocks.append(block)

        files_bool = not files_bool
        i += block[1]

    # iterate from the end to shift blocks into gaps if possible
    # manual indexing since the list disk_blocks is getting modified
    k_block = len(disk_blocks) - 1
    while k_block >= 0:
        block = disk_blocks[k_block]

        # ensure we're trying to move a block
        if block[0] is None:
            k_block -= 1
            continue

        # pick out a gap they can shift into
        found_gap = False
        for k_gap in range(k_block):
            gap = disk_blocks[k_gap]

            # make sure it's a gap
            if gap[0] is not None:
                continue

            # accept if it's big enough
            if gap[1] >= block[1]:
                found_gap = True
                break

        # if there isn't anything to shift into, move on to the next block in the queue
        if not found_gap:
            k_block -= 1
            continue

        # if there is, then do the switcheroos
        block_file_id = block[0]
        block_size = block[1]
        gap_size = gap[1]
        new_gap_size = gap_size - block_size

        # swap the block for a gap
        disk_blocks[k_block] = (None, block_size)

        # swap the gap for a block and a smaller gap
        disk_blocks.pop(k_gap)
        disk_blocks.insert(k_gap, (None, new_gap_size))
        disk_blocks.insert(k_gap, (block_file_id, block_size))

        # no need to decrement k_block because 1 pop + 2 inserts = 1 extra element in the list
        # so we automatically get moved one element lower in disk_blocks

    # convert to a list giving the disk, with zeros for gaps
    disk = []
    for block in disk_blocks:
        file_id = block[0]
        size = block[1]
        if file_id is None:
            file_id = 0
        disk.extend([file_id] * size)

    # compute answer
    soln = int(sum(np.array(disk) * np.array(range(len(disk)))))

    return soln


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
