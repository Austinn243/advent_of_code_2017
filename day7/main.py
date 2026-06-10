"""
Advent of Code 2017, Day 7
Recursive Circus
http://adventofcode.com/2017/day/7
"""

import re
from collections import Counter
from pathlib import Path
from typing import NamedTuple

PROGRAM_REGEX = r"^(\w+) \((\d+)\)(?: -> (.+))?$"

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


class Program(NamedTuple):
    """A program in the tower of programs."""

    name: str
    weight: int
    held_programs: list[str]


def read_programs(file_path: Path) -> list[Program]:
    """Read information about programs from a file."""

    programs: list[Program] = []
    for index, line in enumerate(file_path.open("r", encoding="utf-8")):
        match = re.match(PROGRAM_REGEX, line.strip())
        if not match:
            raise ValueError(f"Invalid line at {index + 1}: {line.strip()}")

        name, weight_str, holds_str = match.groups()
        weight = int(weight_str)
        holds = holds_str.split(", ") if holds_str else []

        program = Program(name=name, weight=weight, held_programs=holds)
        programs.append(program)

    return programs


def find_root_program(programs: list[Program]) -> str:
    """Find the name of the program at the bottom of the tower."""

    candidates = {program.name for program in programs}
    for _, _, held_programs in programs:
        for held_program in held_programs:
            candidates.discard(held_program)

    return candidates.pop()


def find_tower_weights(programs: list[Program]) -> dict[str, int]:
    """Calculate the total weight of each tower in the structure."""

    programs_by_name = {program.name: program for program in programs}
    tower_weights: dict[str, int] = {}

    def calculate_tower_weight(tower_root_name: str) -> int:
        tower_root_program = programs_by_name[tower_root_name]
        if tower_root_name in tower_weights:
            return tower_weights[tower_root_name]

        if not tower_root_program.held_programs:
            tower_weights[tower_root_name] = tower_root_program.weight
            return tower_weights[tower_root_name]

        subtower_weights = [
            calculate_tower_weight(held_program)
            for held_program in tower_root_program.held_programs
        ]
        tower_weights[tower_root_name] = tower_root_program.weight + sum(
            subtower_weights,
        )
        return tower_weights[tower_root_name]

    for program in programs:
        calculate_tower_weight(program.name)

    return tower_weights


def find_weight_adjustment(
    programs: list[Program],
    tower_weights: dict[str, int] | None = None,
) -> int:
    """Find the new weight for the unbalanced program to balance the tower."""

    if tower_weights is None:
        tower_weights = find_tower_weights(programs)

    programs_by_name = {program.name: program for program in programs}
    root_program = programs_by_name[find_root_program(programs)]
    subtower_weights = Counter(
        tower_weights[held_program] for held_program in root_program.held_programs
    )
    if len(subtower_weights) == 1:
        raise ValueError("The tower is already balanced.")

    if len(subtower_weights) > 2:
        raise ValueError("The tower contains more than one unbalanced program.")

    (expected_subtower_weight, _), (unbalanced_subtower_weight, _) = (
        subtower_weights.most_common()
    )
    weight_adjustment = expected_subtower_weight - unbalanced_subtower_weight
    return weight_adjustment


def find_balanced_weight_for_unbalanced_program(programs: list[Program]) -> int:
    """Find the new weight for the unbalanced program to balance the tower."""

    programs_by_name = {program.name: program for program in programs}
    tower_weights = find_tower_weights(programs)
    weight_adjustment = find_weight_adjustment(programs, tower_weights)
    if weight_adjustment == 0:
        raise ValueError("The tower is already balanced.")

    current_program = programs_by_name[find_root_program(programs)]
    while current_program.held_programs:
        subtower_weights = {
            held_program: tower_weights[held_program]
            for held_program in current_program.held_programs
        }
        weight_counts = Counter(subtower_weights.values())
        if len(weight_counts) == 1:
            return current_program.weight + weight_adjustment

        if len(weight_counts) > 2:
            raise ValueError("The tower contains more than one unbalanced program.")

        unbalanced_subtower_weight = weight_counts.most_common()[-1][0]
        current_program = next(
            programs_by_name[held_program]
            for held_program, weight in subtower_weights.items()
            if weight == unbalanced_subtower_weight
        )

    raise ValueError("Unable to determine the balanced weight.")


def main() -> None:
    """Execute the program."""

    input_file = INPUT_FILE
    file_path = Path(__file__).parent / input_file

    programs = read_programs(file_path)

    root_program_name = find_root_program(programs)
    print("The name of the program at the bottom of the tower is:")
    print(root_program_name)
    print()

    rebalanced_weight = find_balanced_weight_for_unbalanced_program(programs)
    print("To balance the tower, the weight of the unbalanced program should be:")
    print(rebalanced_weight)


if __name__ == "__main__":
    main()
