import logging
import pathlib

from aoc.puzzle_input import read_input
from aoc.solver import solver


def first_empty(file_system: list[int], minbound: int) -> int:
    cursor = minbound

    while cursor < len(file_system):
        if file_system[cursor] == -1:
            return cursor

        cursor += 1

    return -1


def last_non_empty(file_system: list[int], maxbound: int) -> int:
    cursor = maxbound

    while cursor >= 0:
        if file_system[cursor] > -1:
            return cursor

        cursor -= 1

    return -1


def move_bit(file_system: list[int], source: int, target: int):
    assert 0 <= source < len(file_system)
    assert 0 <= target < len(file_system)

    file_system[target] = file_system[source]
    file_system[source] = -1


def empty_span(file_system: list[int], minbound: int, maxbound: int) -> tuple[int, int, int, bool]:
    left = first_empty(file_system, minbound)

    if left < 0:
        return -1, -1, -1, False

    right = left

    while True:
        next_index = right + 1

        if next_index > maxbound:
            return -1, -1, -1, False

        if file_system[next_index] != -1:
            return left, right, right - left + 1, True

        right = next_index


def file_span(file_system: list[int], minbound: int, maxbound: int) -> tuple[int, int, int, bool]:
    right = last_non_empty(file_system, maxbound)

    if right < 0:
        return -1, -1, -1, False

    left = right

    while True:
        next_index = left - 1

        if next_index < minbound:
            return -1, -1, -1, False

        if file_system[next_index] != file_system[right]:
            return left, right, right - left + 1, True

        left = next_index


def move_file(file_system: list[int], empty_span: tuple[int, int], file_span: tuple[int, int]):
    for i in range(file_span[1] - file_span[0] + 1):
        move_bit(file_system, file_span[0] + i, empty_span[0] + i)


def trim_empty(file_system: list[int]) -> list[int]:
    if len(file_system) == 0:
        return []

    cursor = len(file_system)

    while file_system[cursor - 1] == -1:
        cursor -= 1

    return file_system[0:cursor]


def find_free_space(file_system: list[int], minbound: int, maxbound: int, minsize: int) -> tuple[int, int, int, bool]:
    left = minbound

    while left <= maxbound:
        if file_system[left] != -1:
            left += 1
            continue

        right = left

        while right <= maxbound:
            next_index = right + 1

            if file_system[next_index] >= 0:
                break

            right = next_index

        size = right - left + 1

        if size >= minsize:
            return left, right, right - left + 1, True
        else:
            left = right + 1
            right = left

    return -1, -1, -1, False


def file_system_to_string(file_system: list[int]) -> str:
    output = ""

    for x in file_system:
        if x == -1:
            output += "."
        else:
            output += str(x)

    return output


def compress_file_system(file_system: list[int]) -> list[int]:
    logging.debug(f"{file_system_to_string(file_system)}")

    file_left, file_right, file_size, file_ok = file_span(file_system, 0, len(file_system) - 1)

    logging.debug(f"file span: {file_left=}, {file_right=}")

    while file_ok:
        empty_left, empty_right, empty_size, empty_ok = find_free_space(file_system, 0, file_left - 1, file_size)

        if empty_ok:
            logging.debug(f"compress {empty_size=} {file_size=}")
            logging.debug(f"  target: ({empty_left}, {empty_right}) {file_system[empty_left:empty_right+1]}")
            logging.debug(f"  source: ({file_left}, {file_right}) {file_system[file_left:file_right+1]}")

            move_file(file_system, (empty_left, empty_right), (file_left, file_right))

            logging.debug(f"{file_system_to_string(file_system)}")

        file_left, file_right, file_size, file_ok = file_span(file_system, 0, file_left - 1)

    return trim_empty(file_system)


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
        if value != -1:
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
