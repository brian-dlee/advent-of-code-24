import logging
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines_v2
from aoc.solver import solver


def move_up(p: g.Point):
    return p[0], g.move_up(p[1])


def move_right(p: g.Point):
    return g.move_right(p[0]), p[1]


def move_down(p: g.Point):
    return p[0], g.move_down(p[1])


def move_left(p: g.Point):
    return g.move_left(p[0]), p[1]


def find_peaks(grid: g.Grid, position: g.Point) -> int:
    current_elevation = int(grid.get(position))

    if current_elevation == 9:
        return 1

    next_elevation = current_elevation + 1
    peaks: int = 0

    p = move_up(position)
    if grid.is_in_bounds(p):
        v = int(grid.get(p))
        if v == next_elevation:
            peaks += find_peaks(grid, p)

    p = move_right(position)
    if grid.is_in_bounds(p):
        v = int(grid.get(p))
        if v == next_elevation:
            peaks += find_peaks(grid, p)

    p = move_down(position)
    if grid.is_in_bounds(p):
        v = int(grid.get(p))
        if v == next_elevation:
            peaks += find_peaks(grid, p)

    p = move_left(position)
    if grid.is_in_bounds(p):
        v = int(grid.get(p))
        if v == next_elevation:
            peaks += find_peaks(grid, p)

    return peaks


def solve(input_file: pathlib.Path) -> str:
    trailheads: list[g.Point] = []

    rows = list(read_input_lines_v2(input_file))
    grid = g.Grid(rows)

    for y, row in grid:
        for x, col in row:
            if col == "0":
                trailheads.append((x, y))

    logging.debug(f"{trailheads=}")

    result: int = 0

    for trailhead in trailheads:
        result += find_peaks(grid, trailhead)

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
