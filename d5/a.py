import logging
import pathlib

from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    rules: list[tuple[int, int]] = []
    updates: list[list[int]] = []

    in_rules = True
    for line in read_input_lines(input_file):
        line = line.strip()

        if line == "":
            in_rules = False
            continue

        if in_rules:
            left, right = line.split("|")
            rules.append((int(left), int(right)))
        else:
            updates.append(list(map(int, line.split(","))))

    logging.debug("rules, count is", len(rules))
    for pair in rules:
        logging.debug(f" - {pair}")

    for update_i, update in enumerate(updates):
        logging.debug("update", update_i)

        pages = set(update)
        valid_rules: list[tuple[int, int]] = []

        for left, right in rules:
            if left in pages and right in pages:
                valid_rules.append((left, right))

        logging.debug(f"current page updates: {update}")
        logging.debug(f"valid rules: {valid_rules}")

        is_ok = True

        for left, right in valid_rules:
            if update.index(left) > update.index(right):
                is_ok = False
                break

        if is_ok:
            result += update[len(update) // 2]

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
