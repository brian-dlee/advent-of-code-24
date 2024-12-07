import logging
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


def print_grid(
    name: str,
    grid: g.Grid,
    start_position: g.Point,
    start_direction: str,
    visits: set[g.Point],
    path: set[tuple[int, int, str]],
    obstacle: g.Point,
):
    grid_file_path = pathlib.Path(f"data/d6_grids/{name}.txt")

    grid_file_path.parent.mkdir(parents=True, exist_ok=True)

    with grid_file_path.open("w") as fp:
        fp.write("    ")
        for x in range(grid.col_count()):
            if x % 5 == 0:
                fp.write(f"{x:<3} ")
        fp.write("\n")

        for y in range(grid.row_count()):
            if y % 5 == 0:
                fp.write(f"{y:<3} ")
            else:
                fp.write("    ")

            for x in range(grid.col_count()):
                ud = (x, y, "up") in path or (x, y, "down") in path
                lr = (x, y, "left") in path or (x, y, "right") in path

                if (x, y) == start_position:
                    match start_direction:
                        case "up":
                            fp.write("^")
                        case "right":
                            fp.write(">")
                        case "down":
                            fp.write("v")
                        case "left":
                            fp.write("<")
                elif (x, y) == obstacle:
                    fp.write("O")
                elif ud and lr:
                    fp.write("+")
                elif ud:
                    fp.write("|")
                elif lr:
                    fp.write("-")
                elif (x, y) in visits:
                    fp.write("X")
                else:
                    match grid.get((x, y)):
                        case ".":
                            fp.write(".")
                        case "#":
                            fp.write("#")
                        case _:
                            fp.write(".")
            fp.write("\n")


def iter_grid(grid: g.Grid, start_position: g.Point, start_direction: str, obstacle: g.Point):
    next_position = position = start_position
    next_direction = direction = start_direction

    while True:
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

        if not grid.is_in_bounds(next_position):
            break

        if grid.get(next_position) == "#" or next_position == obstacle:
            direction = next_direction
        else:
            position = next_position

        yield position, direction


def is_loop(
    grid: g.Grid,
    start_position: g.Point,
    start_direction: str,
    obstacle: g.Point,
    trace_path: set[tuple[int, int, str]] | None = None,
    trace_visits: set[tuple[int, int]] | None = None,
) -> bool:
    step_count = 0

    trace_path = trace_path or set()
    trace_path.add((start_position[0], start_position[1], start_direction))

    trace_visits = trace_visits or set()
    trace_visits.add(start_position)

    for position, direction in iter_grid(grid, start_position, start_direction, obstacle):
        step_count += 1

        if step_count > 100000:
            raise RuntimeError("infinite loop")

        if (position[0], position[1], direction) in trace_path:
            return True

        trace_path.add((position[0], position[1], direction))
        trace_visits.add(position)

    return False


def assert_is_loop(grid: g.Grid, start_position: g.Point, start_direction: str, obstacle: g.Point) -> None:
    path = set()
    visits = set()

    if not is_loop(grid, start_position, start_direction, obstacle, trace_path=path, trace_visits=visits):
        print_grid("failed_loop", grid, start_position, start_direction, visits, path, obstacle)
        assert False, "did not loop"


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    start_position: g.Point = (0, 0)
    rows: list[str] = []
    visits: set[tuple[int, int]] = set()
    path: set[tuple[int, int, str]] = set()
    position: tuple[int, int] = (0, 0)
    direction: str = "up"

    for y, line in enumerate(read_input_lines(input_file)):
        line = line.strip()

        rows.append(line)

        for x, char in enumerate(line):
            if char == "^":
                visits.add((x, y))
                path.add((x, y, "up"))
                start_position = (x, y)
                position = (x, y)

    logging.debug(f"visits: {visits}\n{'\n'.join(rows)}")

    grid = g.Grid(rows)

    next_position = position
    next_direction = direction
    obstacles = set()

    while True:
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

        if not grid.is_in_bounds(next_position):
            break

        if grid.get(next_position) == "#":
            direction = next_direction
            logging.debug(f"turn {direction}")
        else:
            loop_path = set()
            loop_visits = set()
            loop_detected = False

            try:
                loop_detected = is_loop(
                    grid, position, next_direction, next_position, trace_path=loop_path, trace_visits=loop_visits
                )
            except RuntimeError:
                print("infinite loop")
                print(f"{position=}, {next_direction=}, {next_position=}")
                print_grid(
                    "inifite_loop",
                    grid,
                    position,
                    direction,
                    loop_visits,
                    loop_path,
                    next_position,
                )
                exit(1)

            if loop_detected:
                print_grid(
                    "obstacle_" + str(len(obstacles)),
                    grid,
                    start_position,
                    "up",
                    loop_visits,
                    loop_path,
                    next_position,
                )
                # logging.debug(f"obstacle: {next_position}")
                # logging.debug(f"next_direction: {next_direction}")
                # logging.debug(f"next_position: {next_position}")
                #
                # if next_position not in obstacles:
                #     assert_is_loop(grid, position, next_direction, next_position)
                #
                #     print_grid(
                #         "obstacle_" + str(len(obstacles)),
                #         grid,
                #         start_position,
                #         "up",
                #         potential_visits,
                #         potential_path,
                #         next_position,
                #     )

                obstacles.add(next_position)
                # break

            # potential_path = path.copy()
            # potential_visits = visits.copy()
            # potential_next_position = position
            #
            # potential_path.add((position[0], position[1], next_direction))
            #
            # while True:
            #     match next_direction:
            #         case "up":
            #             potential_next_position = potential_next_position[0], g.move_up(potential_next_position[1])
            #         case "right":
            #             potential_next_position = g.move_right(potential_next_position[0]), potential_next_position[1]
            #         case "down":
            #             potential_next_position = potential_next_position[0], g.move_down(potential_next_position[1])
            #         case "left":
            #             potential_next_position = g.move_left(potential_next_position[0]), potential_next_position[1]
            #
            #     if not grid.is_in_bounds(potential_next_position):
            #         logging.debug("leave")
            #         break
            #
            #     logging.debug(f"{potential_next_position}, {grid.get(potential_next_position)}")
            #
            #     if grid.get(potential_next_position) == "#":
            #         logging.debug("leave")
            #         break
            #
            #     potential_path.add((potential_next_position[0], potential_next_position[1], next_direction))
            #     potential_visits.add(potential_next_position)
            #
            #     if (potential_next_position[0], potential_next_position[1], next_direction) in path:

            position = next_position
            visits.add(position)

            logging.debug(f"step {position}")

        path.add((position[0], position[1], direction))

    if start_position in obstacles:
        obstacles.remove(start_position)

    result = len(obstacles)

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
