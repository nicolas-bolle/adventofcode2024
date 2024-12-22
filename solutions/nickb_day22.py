"""Day 22

Runs in 25 seconds
"""

# pylint: disable=invalid-name, redefined-outer-name

from collections import defaultdict
import numpy as np

from utils.inputs import get_input

DAY = 22

MODULUS = 16777216


def step(x: int) -> int:
    """One step in the secret number evolution"""
    y = x * 64
    x = (x ^ y) % MODULUS

    y = x // 32
    x = (x ^ y) % MODULUS

    y = x * 2048
    x = (x ^ y) % MODULUS

    return x


def steps(x, n):
    """Multiple steps in the secret number evolution"""
    for _ in range(n):
        x = step(x)
    return x


def solution_part1(s: str) -> int:
    """Part 1 solution from the plaintext input"""
    secret_numbers = [int(x) for x in s.strip().split()]
    secret_numbers = [steps(x, 2000) for x in secret_numbers]
    return sum(secret_numbers)


def solution_part2(s: str) -> int:
    """Part 2 solution from the plaintext input"""
    secret_numbers = [int(x) for x in s.strip().split()]

    # this variable will track the prices of bananas for each 'round'
    rounds = [[x % 10 for x in secret_numbers]]

    # populate the prices
    for _ in range(2000):
        secret_numbers = [step(x) for x in secret_numbers]
        rounds.append([x % 10 for x in secret_numbers])

    # convert to a numpy array
    # prices.shape = (1811, 2001)
    prices = np.array(rounds).transpose()

    # get the changes in prices
    # diffs.shape = (1811, 2000)
    diffs = np.diff(prices, axis=1)

    # this will keep track of which sequences of prices we've seen for each monkey
    # that way we only buy the first time the sequence comes up (per monkey)
    seen = set()

    # a dictionary that maps sequences of 4 diffs to the number of bananas they give us
    sequences_to_bananas = defaultdict(int)

    # iterate over sequences of 4 diffs to populate the dictionary
    for i in range(diffs.shape[1] - 3):
        # the sequences of 4 diffs that appear
        sequences = diffs[:, i : i + 4]

        # the corresponding numbers of bananas each gives us
        bananas = prices[:, i + 4]

        # go through and "log" each one
        for i, (seq, banana) in enumerate(zip(sequences.tolist(), bananas.tolist())):
            seq = tuple(seq)
            if (i, seq) not in seen:
                sequences_to_bananas[seq] += banana
            seen.add((i, seq))

    # the most bananas obtained out of all the sequences
    most_bananas = max(sequences_to_bananas.values())

    return most_bananas


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
