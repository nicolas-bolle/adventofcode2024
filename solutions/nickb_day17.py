"""Day 17

Part 2 took a while, but I learned to make generators!

I made an object for part 1 to keep things organized

Part 2:
- After a while I realized what the part 1 and part 2 programs were doing
    - 'A' is the "timer" for when the program halts
    - Each run through the instructions prints one output
    - The 'adv' instructions are just bit shifts of 'A'
    - Part 2 always bit shifted by 3
    - Early outputs of the program can depend on a lot of bits of 'A'
    - Later outputs of the program only depend on the most significant bits of 'A'
- Given that, the solution was
    - Think about 'A' as a list of base 8 numbers
    - For each set of numbers, we can find the numbers the program outputs (see nums_to_nums())
    - To find the 'A', iterate starting with the most significant digit of 'A'

One detail is that the most significant digit of 'A' "matches up" with the final instruction and
    final output, so there's some reverses thrown in

And using generators ('yield' and 'yield from') in the search() function made things pretty clean
"""

# pylint: disable=invalid-name, redefined-outer-name

from typing import Generator
import re

from utils.inputs import get_input

DAY = 17


class Computer:
    """A computer istance, intialized from the A, B, C, and program values
    Can .run() the program and report the out_list
    """

    A: int
    B: int
    C: int
    program: list[int]
    instructions: dict[int, callable]
    out_list: list[int]
    i: int

    def __init__(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.program = program

        self.instructions = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

        self.out_list = []

        self.i = 0

    def __str__(self):
        if self.i >= len(self.program):
            status_str = "terminated"
        else:
            status_str = f"{self.i=}"
        return (
            f'Register A: {self.A}\n'
            f'Register B: {self.B}\n'
            f'Register C: {self.C}\n'
            '\n'
            f'Program: {','.join(map(str, self.program))}\n'
            f'Output: {','.join(map(str, self.out_list))}\n'
            f'Status: {status_str}'
        )

    def run(self):
        """Run the program until termination"""
        while self.i < len(self.program):
            self.step()

    def step(self):
        """A single step in the program"""
        instruction, operand = self.program[self.i], self.program[self.i + 1]
        self.instructions[instruction](operand)

    def adv(self, operand: int):
        # self.A = self.A // (2**self.combo_operand(operand))
        self.A = self.A >> self.combo_operand(operand)
        self.i += 2

    def bxl(self, operand: int):
        self.B = self.B ^ self.literal_operand(operand)
        self.i += 2

    def bst(self, operand: int):
        self.B = self.combo_operand(operand) % 8
        self.i += 2

    def jnz(self, operand: int):
        if self.A:
            self.i = self.literal_operand(operand)
        else:
            self.i += 2

    def bxc(self, operand: int):
        self.B = self.B ^ self.C
        self.i += 2

    def out(self, operand: int):
        self.out_list.append(self.combo_operand(operand) % 8)
        self.i += 2

    def bdv(self, operand: int):
        self.B = self.A >> self.combo_operand(operand)
        self.i += 2

    def cdv(self, operand: int):
        self.C = self.A >> self.combo_operand(operand)
        self.i += 2

    def literal_operand(self, operand: int) -> int:
        """Get the literal operand correspnding to 'operand'"""
        if operand > 7:
            raise Exception(f"Unrecognized literal operand {operand}")
        return operand

    def combo_operand(self, operand: int) -> int:
        """Get the combo operand correspnding to 'operand'"""
        match operand:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise Exception("Encountered combo operand 7")
            case _:
                raise Exception(f"Unrecognized combo operand {operand}")
        return operand


def parse_input(s: str) -> tuple[int, int, int, list[int]]:
    """Parse the input into (A, B, C, program)"""
    digits = [int(t) for t in re.findall(r"-?\d+", s)]
    A = digits[0]
    B = digits[1]
    C = digits[2]

    program = digits[3:]

    return A, B, C, program


def nums_to_int(nums: list[int]) -> int:
    """Turn a list of base 8 nums into an int"""
    A = 0
    for num in nums:
        A = (A << 3) + num
    return A


def nums_to_nums(
    A: int,
    B: int,
    C: int,
    program: list[int],
    nums: list[int],
) -> list[int]:
    """Runs a list of base 8 nums "through" the program, outputting the output base 8 nums
    Does this by setting A according to the base 8 nums
    """
    # form the A to use
    A = nums_to_int(nums)

    # run the program
    c = Computer(A, B, C, program)
    c.A = A
    c.run()

    # return the output from last to first
    return list(reversed(c.out_list))


# need to pick the 16 blocks for A
# so for each position, try the values in range(8)
# prune if a place doesn't line up like it should
def search(
    A: int,
    B: int,
    C: int,
    program: list[int],
    nums_target: list[int],
    nums: list[int],
    i: int,
) -> Generator:
    """Search for the smallest A (in nums) that gives nums_actual == nums_target"""

    # base case
    if i == len(nums_target):
        yield nums
        return

    # ensure max length
    if i:
        num_start = 0
    else:
        num_start = 1

    # recursive
    for num in range(num_start, 8):
        nums[i] = num
        nums_actual = nums_to_nums(A, B, C, program, nums)
        if nums_actual[i] == nums_target[i]:
            yield from search(A, B, C, program, nums_target, nums, i + 1)

    # keep things tidy
    nums[i] = 0


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    # parse into a Computer object
    A, B, C, program = parse_input(s)
    c = Computer(A, B, C, program)

    # run the program
    c.run()

    # format the outputs of the program
    out_list = c.out_list
    out_list_str = ",".join(map(str, out_list))

    return out_list_str


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    A, B, C, program = parse_input(s)

    # target numbers: the program in reverse order
    nums_target = list(reversed(program))

    # search for the first nums (list of base 8 nums) representing A that gives nums_target
    gen = search(A, B, C, program, nums_target, [0] * len(nums_target), 0)
    nums = next(gen)

    # convert to an int
    A = nums_to_int(nums)

    return str(A)


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
