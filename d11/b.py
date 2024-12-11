import pathlib

from aoc.puzzle_input import read_input
from aoc.solver import solver


def blink(stone: int, cache: dict[tuple[int, int], int], depth: int) -> int:
    if depth == 0:
        cache[(stone, depth)] = 1
        return 1

    if (stone, depth) in cache:
        return cache[(stone, depth)]

    next_depth = depth - 1

    if stone == 0:
        result = blink(1, cache, next_depth)
    elif len(str(stone)) % 2 == 0:
        value = str(stone)

        lh = int(value[: len(value) // 2])
        lc = blink(lh, cache, next_depth)

        rh = int(value[len(value) // 2 :])
        rc = blink(rh, cache, next_depth)

        result = lc + rc
    else:
        next_stone = stone * 2024
        result = blink(next_stone, cache, next_depth)

    cache[(stone, depth)] = result

    return result


def solve(input_file: pathlib.Path) -> str:
    cache: dict[tuple[int, int], int] = {}
    stones = list(map(int, read_input(input_file).strip().split()))

    result: int = 0

    for stone in stones:
        result += blink(stone, cache, 75)

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
