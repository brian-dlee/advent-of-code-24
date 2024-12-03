import logging
import pathlib
import re

from aoc.puzzle_input import read_input
from aoc.solver import solver


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    text = read_input(input_file).rstrip()

    for match in re.finditer(r"mul\((\d+),(\d+)\)", text):
        a = int(match.group(1))
        b = int(match.group(2))

        result += a * b

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
