"""Testing my solution files match the answers in answers.toml
Assumes this file is in the folder with solution files and answers.toml

The key functions are
test_all()
test_day()
test_file()
"""

# pylint: disable=bare-except

import os
import sys
import importlib
import time
import toml
from utils.inputs import get_input

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

ANSWERS_TOML = "answers.toml"

# listing out the days, actual solutions, and my solution files
CONFIG = [
    # (day, file name)
    (1, "nickb_day1.py"),
    (2, "nickb_day2.py"),
    (3, "nickb_day3.py"),
    (4, "nickb_day4.py"),
    # (5, "nickb_day5.py"),
    (5, "nickb_day5_2.py"),
    # (6, "nickb_day6.py"),
    (6, "nickb_day6_2.py"),
    # (7, "nickb_day7.py"),
    (7, "nickb_day7_2.py"),
    (8, "nickb_day8.py"),
    # (9, "nickb_day9.py"),
    (9, "nickb_day9_2.py"),
    (10, "nickb_day10.py"),
    (11, "nickb_day11.py"),
    (12, "nickb_day12.py"),
    (13, "nickb_day13.py"),
    (14, "nickb_day14.py"),
    (15, "nickb_day15.py"),
    (16, "nickb_day16.py"),
    (17, "nickb_day17.py"),
    (18, "nickb_day18.py"),
    (19, "nickb_day19.py"),
    (20, "nickb_day20.py"),
    (21, "nickb_day21.py"),
    (22, "nickb_day22.py"),
    (23, "nickb_day23.py"),
    # (24, "nickb_day24.py"),
    (25, "nickb_day25.py"),
]

# add current path to system path to simplify module imports
sys.path.append(CURRENT_DIRECTORY)

with open(os.path.join(CURRENT_DIRECTORY, ANSWERS_TOML), "r", encoding="utf-8") as f:
    ANSWERS = toml.load(f)


def test_all() -> bool:
    """Test all solutions"""
    success = True
    for line in CONFIG:
        success = success & test_solution(*line)
        print()
    return success


def test_day(day: int) -> bool:
    """Test all solutions for the given day"""
    lines = []
    for line in CONFIG:
        if line[0] == day:
            lines.append(line)
    assert len(lines) >= 1, f"Day {day} not found in config"
    success = True
    for line in lines:
        success = success & test_solution(*line)
        print()
    return success


def test_file(file_name: str) -> bool:
    """Test the solutions for the given file name"""
    lines = []
    for line in CONFIG:
        if line[-1] == file_name:
            lines.append(line)
    assert len(lines) >= 1, f"File {file_name} not found in config"
    assert len(lines) <= 1, f"File {file_name} found multiple times in config"
    return test_solution(*line)


def test_solution(day, file_name) -> bool:
    """Test a solution, print a report, return a boolean for whether it succeeded"""
    # load the answers
    assert str(day) in ANSWERS, f"{ANSWERS_TOML} does not have a solution for day {day}"
    part_1_soln, part_2_soln = ANSWERS[str(day)]

    # import solution functions
    module_name = file_name.removesuffix(".py")
    module = importlib.import_module(module_name)
    solution_part1 = module.solution_part1
    solution_part2 = module.solution_part2

    s = get_input(day)

    # part 1
    start = time.time()
    try:
        part_1_answer = solution_part1(s)
        part_1_errored = False
    except:
        part_1_answer = None
        part_1_errored = True
    end = time.time()
    part_1_seconds = end - start
    if isinstance(part_1_soln, str):
        # cast answer to string if the solution is a string
        part_1_correct = bool(str(part_1_answer) == part_1_soln)
    else:
        part_1_correct = bool(part_1_answer == part_1_soln)

    # part 2
    start = time.time()
    try:
        part_2_answer = solution_part2(s)
        part_2_errored = False
    except:
        part_2_answer = None
        part_2_errored = True
    end = time.time()
    part_2_seconds = end - start
    if isinstance(part_2_soln, str):
        # cast answer to string if the solution is a string
        part_2_correct = bool(str(part_2_answer) == part_2_soln)
    else:
        part_2_correct = bool(part_2_answer == part_2_soln)

    overall_correct = part_1_correct and part_2_correct

    # print a report
    print("--------------------")
    print(f"Day {day}: {file_name}")
    print("--------------------")
    if part_1_errored:
        print("Part 1: ERRORED")
    else:
        if part_1_correct:
            print(f"Part 1: correct ({part_1_soln})")
        else:
            print(f"Part 1: INCORRECT (expected {part_1_soln} gave {part_1_answer})")
    if part_2_errored:
        print("Part 2: ERRORED")
    else:
        if part_2_correct:
            print(f"Part 2: correct ({part_2_soln})")
        else:
            print(f"Part 2: INCORRECT (expected {part_2_soln} gave {part_2_answer})")
    print(f"Part 1 seconds: {part_1_seconds:.2f}")
    print(f"Part 2 seconds: {part_2_seconds:.2f}")

    return overall_correct


if __name__ == "__main__":
    all_correct_bool = test_all()
    if all_correct_bool:
        print("All correct!")
    else:
        print("Some incorrect!")
