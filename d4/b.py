import logging
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def search(gs: g.GridSearch) -> list[g.Segment]:
    origin_x, origin_y = gs.origin
    x, y = gs.origin

    assert gs.grid.is_in_bounds((x, y)), "origin is not in bounds"

    result: list[g.Segment] = []
    coords: g.Segment = []
    next_char = "X"

    while True:
        if gs.grid.get((x, y)) != next_char:
            next_char = "M"
            coords = []

        if gs.grid.get((x, y)) == next_char:
            coords.append((x, y))

            match next_char:
                case "M":
                    next_char = "A"
                case "A":
                    next_char = "S"
                case "S":
                    next_char = "M"
                    result.append(coords)
                    coords = []

        x, y = gs.step_fn(x, y)

        if not gs.grid.is_in_bounds((x, y)):
            origin_x, origin_y = gs.next_fn(origin_x, origin_y)
            x, y = origin_x, origin_y
            next_char = "X"

            if not gs.grid.is_in_bounds((x, y)):
                break

    return result


def is_an_x(grid: g.Grid, segment: g.Segment) -> bool:
    middle = segment[1]

    assert grid.get(middle) == "A"

    ul = middle[0] - 1, middle[1] - 1
    ur = middle[0] + 1, middle[1] - 1
    bl = middle[0] - 1, middle[1] + 1
    br = middle[0] + 1, middle[1] + 1

    if ul not in segment and br not in segment:
        if grid.get(ul) == "M" and grid.get(br) == "S":
            return True
        if grid.get(ul) == "S" and grid.get(br) == "M":
            return True

    if ur not in segment and bl not in segment:
        if grid.get(ur) == "M" and grid.get(bl) == "S":
            return True
        if grid.get(ur) == "S" and grid.get(bl) == "M":
            return True

    return False


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    rows: list[str] = []
    for line in read_input_lines(input_file):
        rows.append(line.strip())

    grid = g.Grid(rows)
    segments = search(g.GridSearch.diagonal_ul_br_search(grid)) + search(g.GridSearch.diagonal_br_ul_search(grid))

    logging.debug(f"found {len(segments)} ul to br MAS segments")

    for segment in segments:
        if is_an_x(grid, segment):
            result += 1

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
