"""
Advent of Code 2017, Day 3
Spiral Memory
http://adventofcode.com/2017/day/3
"""

INPUT = 361527

def distance_to_center(address: int) -> int:
    """Calculate the distance from a memory address to the center of the spiral grid.
    
    The shortest path to the center of the spiral grid is the Manhattan distance
    between the memory address and the center of the grid.
    """

    pass


def main() -> None:
    """Calculate information about the spiral grid based on a given memory address."""

    address = INPUT

    distance_to_center = distance_to_center(address)
    print(distance_to_center)


if __name__ == '__main__':
    main()