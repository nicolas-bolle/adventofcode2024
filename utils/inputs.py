"""Util for getting input files

To get this working:
- Log into your Advent of Code account
- Visit a url like https://adventofcode.com/2024/day/1/input
- Use browser Inspect to view the cookies sent with your url request
    - Something like "_ga=GA..."
- Create a file cookies.txt in the same directory as inputs.py
- Add the (plaintext) cookies to the file
"""

# pylint: disable=logging-fstring-interpolation

import logging
import datetime
import os
import requests

logger = logging.getLogger(__name__)

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
        logger.debug("Retrieving from website")
        url = f"https://adventofcode.com/2024/day/{day}/input"
        s = requests.get(url, cookies=cookies, headers={}, timeout=10).text
        logger.debug(f"{file_path=}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(s)
        logger.debug(f"Wrote to {file_path}")

    # read the input from the .txt file
    with open(file_path, "r", encoding="utf-8") as file:
        s = file.read()
    logger.debug(f"Retrieved from {file_path}")

    return s.strip()
