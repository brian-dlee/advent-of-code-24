import pathlib
import re

from aoc.puzzle_input import read_input
from aoc.solver import solver


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    text = read_input(input_file).rstrip()
    enabled = True

    for match in re.finditer(r"(mul)\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)", text):
        mul, a, b, do, dont = match.groups()

        if mul and enabled:
            result += int(a) * int(b)
        if do:
            enabled = True
        if dont:
            enabled = False

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
