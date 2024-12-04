import logging
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def search(gs: g.GridSearch) -> int:
    origin_x, origin_y = gs.origin
    x, y = gs.origin

    assert gs.grid.is_in_bounds((x, y)), "origin is not in bounds"

    result = 0
    next_char = "X"

    while True:
        if gs.grid.get((x, y)) != next_char:
            next_char = "X"

        if gs.grid.get((x, y)) == next_char:
            match next_char:
                case "X":
                    next_char = "M"
                case "M":
                    next_char = "A"
                case "A":
                    next_char = "S"
                case "S":
                    next_char = "X"
                    result += 1

        x, y = gs.step_fn(x, y)

        if not gs.grid.is_in_bounds((x, y)):
            origin_x, origin_y = gs.next_fn(origin_x, origin_y)
            x, y = origin_x, origin_y
            next_char = "X"

            if not gs.grid.is_in_bounds((x, y)):
                break

    return result


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    rows: list[str] = []
    for line in read_input_lines(input_file):
        rows.append(line.strip())

    grid = g.Grid(rows)

    vertical_down_result = search(g.GridSearch.vertical_down_search(grid))

    logging.debug(f"{vertical_down_result=}")

    vertical_up_result = search(g.GridSearch.vertical_up_search(grid))

    logging.debug(f"{vertical_up_result=}")

    horizontal_right_result = search(g.GridSearch.horizontal_right_search(grid))

    logging.debug(f"{horizontal_right_result=}")

    horizontal_left_result = search(g.GridSearch.horizontal_left_search(grid))

    logging.debug(f"{horizontal_left_result=}")

    diagonal_ul_br_result = search(g.GridSearch.diagonal_ul_br_search(grid))

    logging.debug(f"{diagonal_ul_br_result=}")

    diagonal_bl_ur_result = search(g.GridSearch.diagonal_bl_ur_search(grid))

    logging.debug(f"{diagonal_bl_ur_result=}")

    diagonal_ur_bl_result = search(g.GridSearch.diagonal_ur_bl_search(grid))

    logging.debug(f"{diagonal_ur_bl_result=}")

    diagonal_br_ul_result = search(g.GridSearch.diagonal_br_ul_search(grid))

    logging.debug(f"{diagonal_br_ul_result=}")

    result = (
        vertical_down_result
        + vertical_up_result
        + horizontal_right_result
        + horizontal_left_result
        + diagonal_ul_br_result
        + diagonal_bl_ur_result
        + diagonal_ur_bl_result
        + diagonal_br_ul_result
    )

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
