import logging
import pathlib

from aoc.color import blue, purple, yellow
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def level_is_safe(direction: int, previous_level: int, level: int) -> bool:
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

    return True


def is_report_safe(levels: list[int]) -> bool:
    if len(levels) <= 1:
        logging.info(f"input   : (n/a) {levels}")

        return True

    direction = 1 if levels[0] < levels[1] else -1
    direction_str = "asc" if direction > 0 else "desc"

    logging.info(f"input   : ({direction_str}) {levels}")

    for i in range(1, len(levels)):
        if not level_is_safe(direction, levels[i - 1], levels[i]):
            return False

    return True


def solve(input_file: pathlib.Path) -> str:
    safe_levels = 0

    for i, line in enumerate(read_input_lines(input_file)):
        line = line.strip()
        levels = list(map(int, line.split()))

        assert len(levels) > 2, "I expected at least 2 levels in each report"

        logging.info(blue(f"report {i}: {line}"))

        is_safe = False

        for i in range(-1, len(levels)):
            copy = [*levels]

            if i >= 0:
                copy.pop(i)
            else:
                logging.warning(yellow(f"[problem dampener] removing element {i} ({levels[i]})"))

            if is_report_safe(copy):
                is_safe = True
                break

        if is_safe:
            logging.info(purple("safe"))
            safe_levels += 1
        else:
            logging.info(purple("not safe"))

    return f"{safe_levels=}"


if __name__ == "__main__":
    solver(solve)
