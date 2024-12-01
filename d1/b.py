import pathlib

from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def split_lr(line: str) -> tuple[int, int]:
    left, right = line.strip().split(maxsplit=2)

    return int(left), int(right)


def solve(input_file: pathlib.Path) -> str:
    location_ids = []
    occurrences = {}

    for ln, rn in map(split_lr, read_input_lines(input_file)):
        location_ids.append(ln)
        occurrences.setdefault(rn, 0)
        occurrences[rn] += 1

    location_ids.sort()

    total_similarity = 0

    for ln in location_ids:
        total_similarity += ln * occurrences.get(ln, 0)

    return f"{total_similarity=}"


if __name__ == "__main__":
    solver(solve)
