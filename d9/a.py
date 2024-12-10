import logging
import pathlib

from aoc.puzzle_input import read_input
from aoc.solver import solver


def first_empty(file_system: list[int], minbound: int) -> int:
    assert 0 <= minbound < len(file_system)

    cursor = minbound

    while cursor < len(file_system):
        if file_system[cursor] == -1:
            return cursor

        cursor += 1

    return 99999999999


def last_non_empty(file_system: list[int], maxbound: int) -> int:
    assert 0 <= maxbound < len(file_system)

    cursor = maxbound

    while cursor >= 0:
        if file_system[cursor] > -1:
            return cursor

        cursor -= 1

    return -99999999999


def move_bit(file_system: list[int], source: int, target: int):
    assert 0 <= source < len(file_system)
    assert 0 <= target < len(file_system)

    file_system[target] = file_system[source]
    file_system[source] = -1


def compress_file_system(file_system: list[int]) -> list[int]:
    left = first_empty(file_system, 0)
    right = last_non_empty(file_system, len(file_system) - 1)

    while True:
        if left >= right:
            break

        move_bit(file_system, right, left)

        left = first_empty(file_system, left)
        right = last_non_empty(file_system, right)

    assert right <= len(file_system), "right ended up too large"

    return file_system[0 : right + 1]


def create_file_system(disk_map: list[int]) -> list[int]:
    file_system: list[int] = []
    block_id = 0

    for i, value in enumerate(disk_map):
        is_block = i % 2 == 0

        if is_block:
            file_system += [block_id] * value
            block_id += 1
        else:
            file_system += [-1] * value

    return file_system


def compute_file_system_checksum(file_system: list[int]) -> int:
    result = 0

    for i, value in enumerate(file_system):
        result += i * value

    return result


def solve(input_file: pathlib.Path) -> str:
    disk_map = list(map(int, read_input(input_file).strip()))

    logging.debug(f"{disk_map=}")

    file_system = create_file_system(disk_map)

    logging.debug(f"{file_system=}")

    assert len(file_system) > 0, "file system is empty"

    file_system = compress_file_system(file_system)

    logging.debug(f"{file_system=}")

    result = compute_file_system_checksum(file_system)

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
