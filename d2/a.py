import logging
import pathlib

from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def is_report_safe(i: int, line: str) -> bool:
    levels = list(map(int, line.strip().split()))

    assert len(levels) > 2, "I expected at least 2 levels in each report"

    direction = 1 if levels[0] < levels[1] else -1
    previous_level = levels[0]

    logging.debug(f"report {i}: {'asc' if direction > 0 else 'desc'}")

    for level in levels[1:]:
        logging.debug(f"{previous_level} -> {level}")

        difference = level - previous_level
        distance = abs(difference)

        logging.debug(f"  {distance=}")

        if distance < 1 or 3 < distance:
            return False

        change = 1 if previous_level < level else -1

        logging.debug(f"  {change=}")

        if direction + change == 0:
            return False

        previous_level = level

    return True


def solve(input_file: pathlib.Path) -> str:
    safe_levels = 0

    for i, line in enumerate(read_input_lines(input_file)):
        line = line.strip()
        is_safe = is_report_safe(i, line)

        if is_safe:
            logging.info(f"safe    : {line}")
            safe_levels += 1
        else:
            logging.info(f"not safe: {line}")

    return f"{safe_levels=}"


if __name__ == "__main__":
    solver(solve)
