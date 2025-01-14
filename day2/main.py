"""
Advent of Code 2017, Day 2
Corruption Checksum
http://adventofcode.com/2017/day/2
"""

from functools import partial
from itertools import product
from os import path
from typing import Callable

INPUT_FILE = "input.txt"

Spreadsheet = list[list[int]]


def read_spreadsheet(file_path: str) -> Spreadsheet:
    """Read a spreadsheet of integers from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [[int(cell) for cell in row.split()] for row in file]


def summarize_spreadsheet(spreadsheet: Spreadsheet, process_row: Callable[[list[int]], int]) -> int:
    """Summarize a spreadsheet using a row processing function."""

    return sum(process_row(row) for row in spreadsheet)


def difference_between_extrema(row: list[int]) -> int:
    """Calculate the difference between the minimum and maximum values in a row."""

    return max(row) - min(row)


def evenly_divisible_quotient(row: list[int]) -> int:
    """Calculate the quotient of the only two numbers in a row that evenly divide each other."""

    for dividend, divisor in product(row, repeat=2):
        if dividend != divisor and dividend % divisor == 0:
            return dividend // divisor
        
    return 0


def main() -> None:
    """Read a spreadsheet from an input file and process it."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    spreadsheet = read_spreadsheet(file_path)
    print(spreadsheet)

    checksum = partial(summarize_spreadsheet, process_row=difference_between_extrema)
    print(checksum(spreadsheet))

    sum_evenly_divisible_quotients = partial(summarize_spreadsheet, process_row=evenly_divisible_quotient)
    print(sum_evenly_divisible_quotients(spreadsheet))


if __name__ == '__main__':
    main()