"""
Advent of Code 2017, Day 6
Memory Reallocation
http://adventofcode.com/2017/day/6
"""

from pathlib import Path

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def read_memory_banks(file_path: Path) -> list[int]:
    """Read memory bank configurations from a file."""

    with file_path.open("r", encoding="utf-8") as file:
        return [int(value) for value in file.read().strip().split()]


def redistribute_memory_banks(memory_banks: list[int]) -> None:
    """Redistribute memory blocks among the banks in-place."""

    max_blocks = max(memory_banks)
    source_index = memory_banks.index(max_blocks)
    memory_banks[source_index] = 0

    for index_offset in range(1, 1 + max_blocks):
        index = (source_index + index_offset) % len(memory_banks)
        memory_banks[index] += 1


def count_redistributions_until_repeat(memory_banks: list[int]) -> int:
    """Count the number of redistributions until a configuration is repeated."""

    seen_distributions: set[tuple[int, ...]] = set()
    current_distribution = memory_banks.copy()
    num_redistributions = 0

    while (
        distribution_signature := tuple(current_distribution)
    ) not in seen_distributions:
        seen_distributions.add(distribution_signature)
        redistribute_memory_banks(current_distribution)
        num_redistributions += 1

    return num_redistributions


def count_loop_cycles(memory_banks: list[int]) -> int:
    """Count the number of cycles within the infinite loop.

    This is equivalent to the number of redistributions between the first occurrence of
    a repeated configuration and its next occurrence.
    """

    distribution_occurrence_cycle: dict[tuple[int, ...], int] = {}
    current_distribution = memory_banks.copy()
    num_redistributions = 0

    while (
        distribution_signature := tuple(current_distribution)
    ) not in distribution_occurrence_cycle:
        distribution_occurrence_cycle[distribution_signature] = num_redistributions
        redistribute_memory_banks(current_distribution)
        num_redistributions += 1

    first_occurrence = distribution_occurrence_cycle[distribution_signature]
    return num_redistributions - first_occurrence


def main() -> None:
    """Execute the program."""

    input_file = INPUT_FILE
    file_path = Path(__file__).parent / input_file

    memory_banks = read_memory_banks(file_path)
    print("Initial memory banks:")
    print(memory_banks)
    print()

    num_redistributions_until_repeat = count_redistributions_until_repeat(memory_banks)
    print("Number of redistributions until a configuration is repeated:")
    print(num_redistributions_until_repeat)
    print()

    num_cycles_in_loop = count_loop_cycles(memory_banks)
    print("Number of cycles in the infinite loop:")
    print(num_cycles_in_loop)


if __name__ == "__main__":
    main()
