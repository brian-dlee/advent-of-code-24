import logging
import os
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


class MoveNotPossibleError(Exception):
    pass


def wait_for_keyboard():
    if os.getenv("WAIT") == "1":
        input("(wait)")


def apply_movement(grid: g.Grid, robot: g.Point, movement: str) -> g.Point:
    logging.debug(f"applying movement: {robot=} {movement=}")

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

    next_position = robot[0] + velocity[0], robot[1] + velocity[1]

    logging.debug(f"  {velocity=}")

    wait_for_keyboard()

    match grid.get(next_position):
        case "#":
            logging.debug("  next position = WALL")

            return robot
        case "[":
            logging.debug("  next position = BOX (LEFT)")

            if can_move_box(grid, next_position, g.translate_right(next_position), velocity):
                logging.debug("  CAN MOVE")

                move_box(grid, next_position, g.translate_right(next_position), velocity)

                apply_shift(grid, robot, velocity)

                return next_position
            else:
                logging.debug("  CANNOT MOVE")

                return robot
        case "]":
            logging.debug("  next position = BOX (RIGHT)")

            if can_move_box(grid, g.translate_left(next_position), next_position, velocity):
                logging.debug("  CAN MOVE")

                move_box(grid, g.translate_left(next_position), next_position, velocity)

                apply_shift(grid, robot, velocity)

                return next_position
            else:
                logging.debug("  CANNOT MOVE")

                return robot
        case ".":
            logging.debug("  next position = EMPTY")

            apply_shift(grid, robot, velocity)

            return next_position
        case x:
            raise ValueError("unexpected grid character: " + x)


def can_move_box(grid: g.Grid, left_half: g.Point, right_half: g.Point, velocity: g.Point) -> bool:
    if velocity[0] < 0:
        direction = "left"
    elif velocity[0] > 0:
        direction = "right"
    else:
        direction = "vertical"

    logging.debug(f"can move box: {left_half=} {right_half=} {velocity=} {direction=}")

    is_move_allowed: bool = False

    match direction:
        case "left":
            next_left_position = g.point_add(left_half, velocity)

            match grid.get(next_left_position):
                case "#":
                    logging.debug("  WALL")

                    is_move_allowed = False
                case "]":
                    logging.debug("  BOX (LEFT SIDE)")

                    is_move_allowed = can_move_box(
                        grid, g.translate_left(next_left_position), next_left_position, velocity
                    )
                case "[":
                    raise RuntimeError("this shouldn't be possible: left_half left translate to [")
                case ".":
                    logging.debug("  EMPTY")

                    is_move_allowed = True
                case x:
                    raise RuntimeError(f"unhandled combo for can_move_box: {x}")

        case "right":
            next_right_position = g.point_add(right_half, velocity)

            match grid.get(next_right_position):
                case "#":
                    logging.debug("  WALL")

                    is_move_allowed = False
                case "]":
                    raise RuntimeError("this shouldn't be possible: right_half right translate to ]")
                case "[":
                    logging.debug("  BOX (RIGHT SIDE)")

                    is_move_allowed = can_move_box(
                        grid, next_right_position, g.translate_right(next_right_position), velocity
                    )
                case ".":
                    logging.debug("  EMPTY")

                    is_move_allowed = True
                case x:
                    raise RuntimeError(f"unhandled combo for can_move_box: {x}")

        case "vertical":
            next_left_position = g.point_add(left_half, velocity)
            next_right_position = g.point_add(right_half, velocity)

            match (grid.get(next_left_position), grid.get(next_right_position)):
                case ("#", _) | (_, "#"):
                    logging.debug("  WALL")

                    is_move_allowed = False
                case ("[", "]"):
                    logging.debug("  BOX (ALIGNED)")

                    is_move_allowed = can_move_box(grid, next_left_position, next_right_position, velocity)
                case ("]", "["):
                    logging.debug("  BOX (TWO BOXES)")

                    is_move_allowed = can_move_box(
                        grid, g.translate_left(next_left_position), next_left_position, velocity
                    )
                    is_move_allowed = is_move_allowed and can_move_box(
                        grid, next_right_position, g.translate_right(next_right_position), velocity
                    )
                case ("]", _):
                    logging.debug("  BOX (RIGHT SIDE)")

                    is_move_allowed = can_move_box(
                        grid, g.translate_left(next_left_position), next_left_position, velocity
                    )
                case (_, "["):
                    logging.debug("  BOX (LEFT SIDE)")

                    is_move_allowed = can_move_box(
                        grid, next_right_position, g.translate_right(next_right_position), velocity
                    )
                case (".", "."):
                    logging.debug("  EMPTY")

                    is_move_allowed = True
                case x:
                    raise RuntimeError(f"unhandled combo for can_move_box: {x}")

        case direction:
            raise ValueError("invalid direction: " + direction)

    logging.debug(f"  {'YES' if is_move_allowed else 'NO'}")

    return is_move_allowed


def move_box(grid: g.Grid, left_half: g.Point, right_half: g.Point, velocity: g.Point) -> None:
    if velocity[0] < 0:
        direction = "left"
    elif velocity[0] > 0:
        direction = "right"
    else:
        direction = "vertical"

    match direction:
        case "left":
            next_left_position = g.point_add(left_half, velocity)

            match grid.get(next_left_position):
                case "#":
                    raise MoveNotPossibleError()
                case "]":
                    move_box(grid, g.translate_left(next_left_position), next_left_position, velocity)
                case "[":
                    raise RuntimeError("this shouldn't be possible: left_half left translate to [")
                case ".":
                    pass
                case x:
                    raise RuntimeError(f"unhandled combo for move_box: {x}")

            grid.setchar(next_left_position, "[")
            grid.setchar(left_half, "]")
            grid.setchar(right_half, ".")

        case "right":
            next_right_position = g.point_add(right_half, velocity)

            match grid.get(next_right_position):
                case "#":
                    raise MoveNotPossibleError()
                case "]":
                    raise RuntimeError("this shouldn't be possible: right_half right translate to ]")
                case "[":
                    move_box(grid, next_right_position, g.translate_right(next_right_position), velocity)
                case ".":
                    pass
                case x:
                    raise RuntimeError(f"unhandled combo for move_box: {x}")

            grid.setchar(next_right_position, "]")
            grid.setchar(right_half, "[")
            grid.setchar(left_half, ".")

        case "vertical":
            next_left_position = g.point_add(left_half, velocity)
            next_right_position = g.point_add(right_half, velocity)

            match (grid.get(next_left_position), grid.get(next_right_position)):
                case ("#", _) | (_, "#"):
                    raise MoveNotPossibleError()
                case ("[", "]"):
                    move_box(grid, next_left_position, next_right_position, velocity)
                case ("]", "["):
                    move_box(grid, g.translate_left(next_left_position), next_left_position, velocity)
                    move_box(grid, next_right_position, g.translate_right(next_right_position), velocity)
                case ("]", _):
                    move_box(grid, g.translate_left(next_left_position), next_left_position, velocity)
                case (_, "["):
                    move_box(grid, next_right_position, g.translate_right(next_right_position), velocity)
                case (".", "."):
                    pass
                case x:
                    raise RuntimeError(f"unhandled combo for move_box: {x}")

            grid.setchar(next_left_position, "[")
            grid.setchar(next_right_position, "]")
            grid.setchar(left_half, ".")
            grid.setchar(right_half, ".")


def apply_shift(grid: g.Grid, position: g.Point, velocity: g.Point):
    next_position = g.point_add(position, velocity)

    if grid.get(next_position) != ".":
        apply_shift(grid, next_position, velocity)

    grid.setchar(next_position, grid.get(position))
    grid.setchar(position, ".")


def must_find_char(grid: g.Grid, char: str) -> g.Point:
    for y, row in grid:
        for x, cell in row:
            if cell == char:
                return (x, y)

    raise RuntimeError("char not found in grid: " + char)


def draw_grid(grid: g.Grid) -> None:
    if os.getenv("DRAW") != "1":
        return

    print()

    if grid.col_count() > 99:
        d3s = "    "

        for x in range(100, grid.col_count()):
            n = str(x)

            if x > 99:
                d3s += n[2]
            else:
                d3s += " "

        print(d3s)

    if grid.col_count() > 9:
        d2s = "    " + " " * 10

        for x in range(10, grid.col_count()):
            n = str(x)

            if x > 9:
                d2s += n[1]
            else:
                d2s += " "

        print(d2s)

    d1s = "    "

    for x in range(grid.col_count()):
        n = str(x)
        d1s += n[0]

    print(d1s)

    for y, row in grid:
        print(f"{y:>3} ", end="")

        for _, cell in row:
            print(cell, end="")

        print()

    print()


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    lines = read_input_lines(input_file)

    rows: list[str] = []
    while True:
        line = next(lines, "")
        line = line.strip()

        if len(line) == 0:
            break

        new_line = ""
        for char in line:
            match char:
                case "O":
                    new_line += "[]"
                case ".":
                    new_line += ".."
                case "#":
                    new_line += "##"
                case "@":
                    new_line += "@."

        rows.append(new_line)

    grid = g.Grid(rows)

    movements = ""
    while True:
        line = next(lines, "")
        line = line.strip()

        if len(line) == 0:
            break

        movements += line

    draw_grid(grid)

    robot = must_find_char(grid, "@")
    for movement in movements:
        robot = apply_movement(grid, robot, movement)

        draw_grid(grid)

        wait_for_keyboard()

    for y, row in grid:
        for x, cell in row:
            if cell == "[":
                result += y * 100 + x

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
