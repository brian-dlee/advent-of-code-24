import logging
import pathlib

from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def fix(rules: list[tuple[int, int]], pages: list[int]) -> list[int]:
    ordering: list[int] = [0] * len(pages)

    for left, right in rules:
        ordering[pages.index(left)] -= 1
        ordering[pages.index(right)] += 1

    return [pair[1] for pair in sorted(zip(ordering, pages), key=lambda pair: pair[0])]


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

        logging.debug(f"current page update: {update}")
        logging.debug(f"valid_rules: {valid_rules}")

        is_ok = True

        for left, right in valid_rules:
            if update.index(left) > update.index(right):
                is_ok = False
                break

        if not is_ok:
            update = fix(valid_rules, update)
            result += update[len(update) // 2]

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
