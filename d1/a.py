import pathlib

from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def split_lr(line: str) -> tuple[int, int]:
    left, right = line.strip().split(maxsplit=2)

    return int(left), int(right)


def solve(input_file: pathlib.Path) -> str:
    location_ids_a = []
    location_ids_b = []

    for ln, rn in map(split_lr, read_input_lines(input_file)):
        location_ids_a.append(ln)
        location_ids_b.append(rn)

    assert len(location_ids_a) == len(location_ids_b), "the length of the lists do not match"

    location_ids_a.sort()
    location_ids_b.sort()

    total_distance = 0

    for i in range(len(location_ids_a)):
        total_distance += abs(location_ids_a[i] - location_ids_b[i])

    return f"{total_distance=}"


if __name__ == "__main__":
    solver(solve)
