"""
Advent of Code 2017, Day 1
Inverse Captcha
http://adventofcode.com/2017/day/1
"""

from os import path
from typing import Callable


INPUT_FILE = "input.txt"


def read_sequence(file_path: str) -> list[int]:
    """Read a sequence of digits from a file and return them as a list."""

    with open(file_path, encoding="utf-8") as file:
        sequence = [int(digit) for digit in file.read().strip()]

    return sequence


def sum_matching_pairs(sequence: list[int], next_digit: Callable[[list[int], int], int]) -> int:
    """Sum the digits that match the next digit in the circular sequence."""

    return sum(digit for i, digit in enumerate(sequence) if digit == next_digit(sequence, i))


def get_following_digit(sequence: list[int], index: int) -> int:
    """Return the digit following the digit at the given index in the sequence."""

    return sequence[(index + 1) % len(sequence)]


def get_halfway_digit(sequence: list[int], index: int) -> int:
    """Return the digit halfway around the circular sequence from the digit at the given index."""

    halfway = len(sequence) // 2
    return sequence[(index + halfway) % len(sequence)]


def main() -> None:
    """Read a sequence of digits from an input file and process them."""

    file = INPUT_FILE
    file_path = path.join(path.dirname(__file__), file)

    sequence = read_sequence(file_path)

    print(sum_matching_pairs(sequence, get_following_digit))
    print(sum_matching_pairs(sequence, get_halfway_digit))


if __name__ == '__main__':
    main()