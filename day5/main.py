"""
Advent of Code 2017, Day 5
A Maze of Twisty Trampolines, All Alike
http://adventofcode.com/2017/day/5
"""

from os import path
from typing import Callable

INPUT_FILE = 'input.txt'


def read_offsets(file_path: str) -> list[int]:
    """Read jump offsets from a file."""

    with open(file_path, encoding='utf-8') as file:
        return [int(line.strip()) for line in file]


def steps_to_exit(jump_offsets: list[int], update_offset: Callable[[int], int]) -> int:
    """Count the number of steps required to exit the maze."""

    jump_offsets = jump_offsets.copy()
    step_count = 0
    index = 0

    while 0 <= index < len(jump_offsets):
        offset = jump_offsets[index]
        next_index = index + offset

        jump_offsets[index] = update_offset(offset)
        index = next_index
        step_count += 1

    return step_count


def main() -> None:
    """Read jump offsets from a file and process them."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    jump_offsets = read_offsets(file_path)
    print(jump_offsets)

    print(steps_to_exit(jump_offsets, lambda offset: offset + 1))
    print(steps_to_exit(jump_offsets, lambda offset: offset + 1 if offset < 3 else offset - 1))


if __name__ == '__main__':
    main()