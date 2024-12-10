"""Day 9

NASTY solution, and slow (10 seconds)
Part 1 was easy, but I really overcomplicated part 2

The way I use the BinaryList object makes things slower
The way I'm using them is really inefficient
But it's left over from my first try when I thought the step of searching
    for a gap to put a block in was going to be a huge bottleneck
"""

# pylint: disable=invalid-name, redefined-outer-name

from typing import Self
from functools import total_ordering

import numpy as np

from utils.inputs import get_input
from utils.utilities import BinaryList

DAY = 9


@total_ordering
class Block:
    """A block on disc memory"""

    file_id: int
    i: int
    size: int

    def __init__(self, file_id: int, i: int, size: int):
        self.file_id = file_id
        self.i = i
        self.size = size

    def __str__(self):
        return f"{self.file_id=} {self.i=} {self.size=}"

    def __iter__(self):
        """Iterable representing the block, but with Nones replaced by zeros"""
        if self.file_id is None:
            file_id = 0
        else:
            file_id = self.file_id
        for _ in range(self.size):
            yield file_id

    def __eq__(self, other: Self):
        return self.i == other.i

    def __lt__(self, other: Self):
        return self.i < other.i


def remove(block, disk_blocks):
    """Remove a block from the BinaryList"""
    disk_blocks.remove(block)


def push(block, disk_blocks):
    """Push a block to the BinaryList
    When pushing a regular block, no issues
    But when pushing a gap, need to make sure to merge it with adjacent gaps!
    """
    disk_blocks.push(block)
    if block.file_id is None:
        merge_gaps(block, disk_blocks)


def merge_gaps(block, disk_blocks):
    """Check if there are gap blocks to the left and right
    If so, merge with them
    """
    if block.file_id is not None:
        return

    # merge right
    k = disk_blocks.find(block)
    if k + 1 < len(disk_blocks) and disk_blocks[k + 1].file_id is None:
        block2 = disk_blocks[k + 1]
        new_block = Block(file_id=None, i=block.i, size=block.size + block2.size)
        remove(block, disk_blocks)
        remove(block2, disk_blocks)
        push(new_block, disk_blocks)
        return

    # merge left
    k = disk_blocks.find(block)
    if 0 <= k - 1 and disk_blocks[k - 1].file_id is None:
        block2 = disk_blocks[k - 1]
        new_block = Block(file_id=None, i=block2.i, size=block.size + block2.size)
        remove(block, disk_blocks)
        remove(block2, disk_blocks)
        push(new_block, disk_blocks)
        return


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
    soln = int(sum(np.array(disk) * np.array(range(len(disk)))))

    return soln


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    # make a BinaryList of Block objects representing the disk
    disk_blocks = BinaryList()
    k = 0
    i = 0
    files_bool = True
    for num in s:
        if files_bool:
            block = Block(file_id=k, i=i, size=int(num))
            k += 1
        else:
            block = Block(file_id=None, i=i, size=int(num))
        files_bool = not files_bool
        i += block.size

        if not block.size == 0:
            disk_blocks.append(block)

    # make a queue of block objects to try shifting left
    blocks_queue = [
        block for block in reversed(disk_blocks) if block.file_id is not None
    ]

    # iterate through queue of blocks, shifting them to the correct spot if possible
    for block in blocks_queue:
        # pick out a gap block they can shift into
        gap_block = None
        for _block in disk_blocks:
            if _block > block:
                break
            if _block.file_id is None and _block.size >= block.size:
                gap_block = _block
                break

        # if there isn't anything to shift into, move on to the next block in the queue
        if gap_block is None:
            continue

        # if there is, then do the switcheroos
        block_file_id = block.file_id
        block_i = block.i
        block_size = block.size
        gap_i = gap_block.i
        gap_size = gap_block.size

        # the gap that will be left over on insert
        new_lower_gap_i = gap_i + block_size
        new_lower_gap_size = gap_size - block_size

        # remove the actual block
        remove(block, disk_blocks)

        # remove the old gap block
        remove(gap_block, disk_blocks)

        # add the new block
        _block = Block(file_id=block_file_id, i=gap_i, size=block_size)
        push(_block, disk_blocks)

        # replace the hole it left behind with a new gap block
        _gap_block = Block(file_id=None, i=block_i, size=block_size)
        push(_gap_block, disk_blocks)

        # add the new gap if needed
        if new_lower_gap_size:
            _gap_block = Block(file_id=None, i=new_lower_gap_i, size=new_lower_gap_size)
            push(_gap_block, disk_blocks)

    # convert to a list giving the disk
    disk = []
    for block in disk_blocks:
        disk.extend(list(block))

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
