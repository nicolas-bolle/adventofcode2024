"""Misc utils for getting and parsing input files"""

import datetime
import os
import requests

import numpy as np

# cookies for url requests, read in from the cookies.txt file
# put your plaintext url request cookies there
cookies = {}
PATH_COOKIES_TXT = os.path.join(os.path.dirname(__file__), "cookies.txt")
with open(PATH_COOKIES_TXT, "r", encoding="utf-8") as file:
    cookies["session"] = file.read().strip()

# file path of the 'inputs' folder for .txt files
FOLDER_INPUTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inputs")


def get_input(day: int = None) -> str:
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


def split(s: str, char: str) -> str:
    """Split string into chunks based on a character"""
    return s.strip().split(char)


def split_newline(s: str) -> list:
    """Split on newline characters"""
    return split(s, "\n")


def split_lax(s: str) -> list:
    """Split string based on common splitting characters: newline, tab, or one or more spaces"""
    # standardize to spaces
    s = s.replace("\n", " ")
    s = s.replace("\t", " ")

    # replace all multi-space character groups with single spaces
    n = len(s) + 1
    while len(s) < n:
        n = len(s)
        s = s.replace("  ", " ")

    # split on (single) spaces
    return split(s, " ")


def list_map(function: callable, iterable: iter, *iterables, **kwargs) -> list:
    """map() but it returns a list instead of an iterable"""
    return list(map(function, iterable, *iterables, **kwargs))


def list_reshape(array: list, shape: tuple) -> list:
    """Reshape a list like a numpy array, and return "listy" things"""
    return np.array(array).reshape(shape).tolist()


CHARS_INT = set(list("1234567890"))


def get_int(s: str) -> int:
    """Attempts to return the first int in a string"""
    n = ""
    started = False
    for char in s:
        if char in CHARS_INT:
            started = True
            n = n + char
        else:
            if started:
                break
    return int(n)


CHARS_FLOAT = set(list("1234567890."))


def get_float(s: str) -> float:
    """Attempts to return the first float in a string"""
    n = ""
    started = False
    for char in s:
        if char in CHARS_FLOAT:
            started = True
            n = n + char
        else:
            if started:
                break
    return float(n)
