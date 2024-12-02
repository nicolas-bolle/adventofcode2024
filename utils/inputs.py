"""Misc utils for getting and parsing input files"""

import datetime
import os
import requests

# cookies for url requests, read in from the cookies.txt file
# put your plaintext url request cookies there
cookies = {}
with open("cookies.txt", "r", encoding="utf-8") as file:
    cookies["session"] = file.read().strip()

# file path of the 'inputs' folder for .txt files
FOLDER_INPUTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inputs")


def get_input(day=None):
    """Get the input for the given date"""
    if day is None:
        date = datetime.datetime.now()
        assert (date >= date.year == 2024) and (
            date.month == 12
        ), "Must be December 2024"
        day = date.day
    assert day <= 31
    file_name = f"input{day}.txt"
    file_path = os.path.join(FOLDER_INPUTS, file_name)

    # if .txt file of input doesn't exist, download from the website
    if not os.path.exists(file_path):
        print("Retrieving from website")
        url = f"https://adventofcode.com/2024/day/{day}/input"
        s = requests.get(url, cookies=cookies, headers={}, timeout=10).text
        print(file_path)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(s)
        print(f"Wrote to {file_path}")

    # read the input from the .txt file
    with open(file_path, "r", encoding="utf-8") as file:
        s = file.read()
    print(f"Retrieved from {file_path}")

    return s.strip()


def split(s, line_char="\n", block_char="\n\n"):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    return out


def get_int(string):
    """Assuming a string contains a single integer, retrieve that int"""
    chars = set(list("1234567890"))
    n = ""
    for char in string:
        if char in chars:
            n = n + char
    return int(n)
