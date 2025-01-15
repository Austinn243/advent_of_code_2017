"""
Advent of Code 2017, Day 4
High-Entropy Passphrases
http://adventofcode.com/2017/day/4
"""

from os import path

INPUT_FILE = "input.txt"


def read_passphrases(file_path: str) -> list[str]:
    """Read passphrases from a file."""

    with open(file_path, encoding="utf-8") as file:
        return [line.strip() for line in file]


def contains_no_duplicates(passphrase: str) -> bool:
    """Determine if a passphrase contains no duplicate words."""

    words = passphrase.split()
    seen = set()

    for word in words:
        if word in seen:
            return False

        seen.add(word)

    return True


def contains_no_anagrams(passphrase: str) -> bool:
    """Determine if a passphrase contains no anagrams."""

    # CONSIDER: This approach works fine for the purposes of this problem but it would
    # be an interesting exercise to see if hashing could be used to improve performance.

    words = passphrase.split()
    seen = set()

    for word in words:
        sorted_chars = sorted(word)
        sorted_word = "".join(sorted_chars)

        if sorted_word in seen:
            return False

        seen.add(sorted_word)

    return True


def main() -> None:
    """Read passphrases from a file and process them."""

    file_path = path.join(path.dirname(__file__), INPUT_FILE)

    passphrases = read_passphrases(file_path)
    print(passphrases)

    passphrase_without_duplicate_count = sum(
        contains_no_duplicates(passphrase) for passphrase in passphrases
    )
    print(passphrase_without_duplicate_count)

    passphrase_without_anagram_count = sum(
        contains_no_anagrams(passphrase) for passphrase in passphrases
    )
    print(passphrase_without_anagram_count)


if __name__ == "__main__":
    main()
