"""
Advent of Code 2017, Day 9
Stream Processing
https://adventofcode.com/2017/day/9
"""

from enum import IntEnum
from pathlib import Path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

GROUP_START = "{"
GROUP_END = "}"
GARBAGE_START = "<"
GARBAGE_END = ">"
CANCEL = "!"


class State(IntEnum):
    """Represents the state of the stream reader."""

    READING_GROUP = 0
    READING_GARBAGE = 1
    CANCELING_NEXT_CHARACTER = 2


def read_stream(file_path: Path) -> str:
    """Read the stream from the file."""

    with file_path.open() as f:
        return f.read().strip()


def find_total_score(stream: str) -> int:
    """Find the total score of all groups in a stream.

    The score of any given group is one more than the score of its parent group.
    The outermost group gets a score of 1.
    """

    depth = 0
    total_score = 0
    state = State.READING_GROUP

    for char in stream:
        match state:
            case State.READING_GROUP:
                if char == GROUP_START:
                    depth += 1
                elif char == GROUP_END:
                    total_score += depth
                    depth -= 1
                elif char == GARBAGE_START:
                    state = State.READING_GARBAGE
            case State.READING_GARBAGE:
                if char == CANCEL:
                    state = State.CANCELING_NEXT_CHARACTER
                elif char == GARBAGE_END:
                    state = State.READING_GROUP
            case State.CANCELING_NEXT_CHARACTER:
                state = State.READING_GARBAGE

    return total_score


def count_garbage_characters(stream: str) -> int:
    """Count the number of non-canceled characters within the garbage in the stream."""

    state = State.READING_GROUP
    garbage_count = 0

    for char in stream:
        match state:
            case State.READING_GROUP:
                if char == GARBAGE_START:
                    state = State.READING_GARBAGE
            case State.READING_GARBAGE:
                if char == CANCEL:
                    state = State.CANCELING_NEXT_CHARACTER
                elif char == GARBAGE_END:
                    state = State.READING_GROUP
                else:
                    garbage_count += 1
            case State.CANCELING_NEXT_CHARACTER:
                state = State.READING_GARBAGE

    return garbage_count


def main() -> None:
    """Execute the program."""

    input_file = INPUT_FILE
    file_path = Path(__file__).parent / input_file

    stream = read_stream(file_path)

    total_score = find_total_score(stream)
    print("The total score of all groups in the stream is:")
    print(total_score)
    print()

    garbage_count = count_garbage_characters(stream)
    print("The total number of non-canceled characters within the garbage is:")
    print(garbage_count)


if __name__ == "__main__":
    main()
