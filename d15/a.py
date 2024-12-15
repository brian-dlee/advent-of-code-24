import logging
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def apply_movement(grid: g.Grid, robot: g.Point, movement: str) -> g.Point:
    match movement:
        case "^":
            velocity = (0, -1)
        case ">":
            velocity = (1, 0)
        case "v":
            velocity = (0, 1)
        case "<":
            velocity = (-1, 0)
        case _:
            raise ValueError("invalid movement code: " + movement)

    return apply_shift(grid, robot, velocity)


def apply_shift(grid: g.Grid, position: g.Point, velocity: g.Point) -> g.Point:
    next_position = position[0] + velocity[0], position[1] + velocity[1]

    match grid.get(next_position):
        case "#":
            return position
        case "O":
            next_box_position = apply_shift(grid, next_position, velocity)
            if next_box_position != next_position:
                grid.setchar(next_position, grid.get(position))
                grid.setchar(position, ".")
                return next_position
            else:
                return position
        case _:
            grid.setchar(next_position, grid.get(position))
            grid.setchar(position, ".")
            return next_position


def must_find_char(grid: g.Grid, char: str) -> g.Point:
    for y, row in grid:
        for x, cell in row:
            if cell == char:
                return (x, y)

    raise RuntimeError("char not found in grid: " + char)


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    lines = read_input_lines(input_file)

    rows: list[str] = []
    while True:
        line = next(lines, "")
        line = line.strip()

        if len(line) == 0:
            break

        rows.append(line)

    grid = g.Grid(rows)

    movements = ""
    while True:
        line = next(lines, "")
        line = line.strip()

        if len(line) == 0:
            break

        movements += line

    robot = must_find_char(grid, "@")

    for movement in movements:
        robot = apply_movement(grid, robot, movement)

        # for _, row in grid:
        #     for _, cell in row:
        #         print(cell, end="")
        #     print()

    for y, row in grid:
        for x, cell in row:
            if cell == "O":
                result += y * 100 + x

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
