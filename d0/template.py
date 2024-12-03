import logging
import pathlib

from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    for line in read_input_lines(input_file):
        line = line.strip()
        line_length = len(line)

        logging.debug(f"length of line: {line_length}")

        result += line_length

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
