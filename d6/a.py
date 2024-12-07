import logging
import pathlib
import sys

from aoc import grid as g
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    rows: list[str] = []
    visits: set[tuple[int, int]] = set()
    position: tuple[int, int] = (0, 0)
    direction: str = "up"

    for i, line in enumerate(read_input_lines(input_file)):
        line = line.strip()

        rows.append(line)

        for j, char in enumerate(line):
            if char == "^":
                visits.add((j, i))
                position = (j, i)

    logging.debug(f"visits: {visits}\n{'\n'.join(rows)}")

    grid = g.Grid(rows)

    next_position = position
    next_direction = direction

    while grid.is_in_bounds(next_position):
        if grid.get(next_position) == "#":
            direction = next_direction
        else:
            position = next_position

        match direction:
            case "up":
                next_direction = "right"
                next_position = position[0], g.move_up(position[1])
            case "right":
                next_position = g.move_right(position[0]), position[1]
                next_direction = "down"
            case "down":
                next_position = position[0], g.move_down(position[1])
                next_direction = "left"
            case "left":
                next_position = g.move_left(position[0]), position[1]
                next_direction = "up"

        visits.add(position)

    sys.stdout.write("\n")
    for i in range(grid.row_count()):
        for j in range(grid.col_count()):
            if (i, j) in visits:
                sys.stdout.write("X")
            else:
                sys.stdout.write(grid.get((i, j)))
        sys.stdout.write("\n")
    sys.stdout.write("\n")

    result = len(visits)

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
