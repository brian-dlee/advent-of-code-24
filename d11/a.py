import pathlib

from aoc.puzzle_input import read_input
from aoc.solver import solver


def blink(stones: list[int]) -> list[int]:
    new_stones: list[int] = []

    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            value = str(stone)
            left = value[: len(value) // 2]
            right = value[len(value) // 2 :]
            new_stones += [int(left), int(right)]
        else:
            new_stones.append(stone * 2024)

    return new_stones


def solve(input_file: pathlib.Path) -> str:
    stones = list(map(int, read_input(input_file).strip().split()))

    for _ in range(25):
        stones = blink(stones)

    result = len(stones)

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
