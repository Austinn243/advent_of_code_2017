"""
Advent of Code 2017, Day 8
I Heard You Like Registers
http://adventofcode.com/2017/day/8
"""

import re
from collections.abc import Callable
from operator import add, eq, ge, gt, le, lt, ne, sub
from pathlib import Path
from typing import NamedTuple

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

CONDITION_MAP: dict[str, Callable[[int, int], bool]] = {
    "==": eq,
    "!=": ne,
    "<": lt,
    ">": gt,
    "<=": le,
    ">=": ge,
}
INSTRUCTION_REGEX = re.compile(
    r"^(\w+) (inc|dec) (-?\d+) if (\w+) (==|!=|<|>|<=|>=) (-?\d+)$",
)
OPERATION_MAP: dict[str, Callable[[int, int], int]] = {
    "inc": add,
    "dec": sub,
}

type Registry = dict[str, int]


class Instruction(NamedTuple):
    """An instruction to modify a register."""

    target_register: str
    operation: Callable[[int, int], int]
    operation_value: int
    condition_register: str
    condition: Callable[[int, int], bool]
    condition_value: int

    def evaluate(self, registry: Registry) -> None:
        """Evaluate the instruction, modifying the registry if the condition is met."""

        target_value = registry.get(self.target_register, 0)
        condition_value = registry.get(self.condition_register, 0)

        condition_satisfied = self.condition(condition_value, self.condition_value)
        if condition_satisfied:
            registry[self.target_register] = self.operation(
                target_value,
                self.operation_value,
            )


def read_instructions(file_path: Path) -> list[Instruction]:
    """Read instructions from a file."""

    instructions: list[Instruction] = []
    for line_number, line in enumerate(file_path.open("r", encoding="utf-8"), start=1):
        match = INSTRUCTION_REGEX.match(line.strip())
        if not match:
            raise ValueError(f"Invalid line at {line_number}: {line.strip()}")

        (
            target_register,
            operation_type,
            operation_value_str,
            condition_register,
            condition_type,
            condition_value_str,
        ) = match.groups()

        operation = OPERATION_MAP.get(operation_type)
        if not operation:
            raise ValueError(
                f"Invalid operation at line {line_number}: {operation_type}",
            )

        condition = CONDITION_MAP.get(condition_type)
        if not condition:
            raise ValueError(
                f"Invalid condition operator at line {line_number}: {condition_type}",
            )

        instruction = Instruction(
            target_register=target_register,
            operation=operation,
            operation_value=int(operation_value_str),
            condition_register=condition_register,
            condition=condition,
            condition_value=int(condition_value_str),
        )
        instructions.append(instruction)

    return instructions


def find_max_final_value(
    instructions: list[Instruction],
    registry: Registry | None = None,
) -> int:
    """Apply instructions to a registry and return the maximum of its final values."""

    if registry is None:
        registry = {}

    for instruction in instructions:
        instruction.evaluate(registry)

    return max(registry.values(), default=0)


def find_max_intermediate_value(
    instructions: list[Instruction],
    registry: Registry | None = None,
) -> int:
    """Apply instructions to a registry and return the maximum value it holds at any point."""

    if registry is None:
        registry = {}

    max_value = 0
    for instruction in instructions:
        instruction.evaluate(registry)
        new_register_value = registry.get(instruction.target_register, 0)
        max_value = max(max_value, new_register_value)

    return max_value


def main() -> None:
    """Run the program."""

    input_file = INPUT_FILE
    file_path = Path(__file__).parent / input_file

    instructions = read_instructions(file_path)
    print(instructions)

    max_final_value = find_max_final_value(instructions)
    print("The largest value in the registry after all instructions is:")
    print(max_final_value)

    max_intermediate_value = find_max_intermediate_value(instructions)
    print("The largest value in the registry during the process is:")
    print(max_intermediate_value)


if __name__ == "__main__":
    main()
