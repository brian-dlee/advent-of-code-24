import pathlib
import re

from aoc.puzzle_input import read_input_lines_v2
from aoc.solver import solver


Robot = tuple[int, int, int, int]
Size = tuple[int, int]


def read_coord_pairs(line: str) -> Robot:
    px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
    return px, py, vx, vy


def move_robot(size: Size, robot: Robot) -> Robot:
    px, py, vx, vy = robot
    return (px + vx) % size[0], (py + vy) % size[1], vx, vy


def draw(size: Size, robots: list[Robot], file_path: pathlib.Path):
    robot_count_by_position: dict[tuple[int, int], int] = {}

    for px, py, _, _ in robots:
        robot_count_by_position.setdefault((px, py), 0)
        robot_count_by_position[(px, py)] += 1

    for _, count in robot_count_by_position.items():
        if count > 1:
            return

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w") as fp:
        for y in range(size[1]):
            for x in range(size[0]):
                if (x, y) in robot_count_by_position:
                    fp.write(str(robot_count_by_position[(x, y)]))
                else:
                    fp.write(" ")
            fp.write("\n")


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    if "_sample" in input_file.name:
        grid_size = (11, 7)
    else:
        grid_size = (101, 103)

    robots: list[Robot] = []
    for px, py, vx, vy in map(read_coord_pairs, read_input_lines_v2(input_file)):
        robots.append((px, py, vx, vy))

    for i in range(10_000):
        new_robots: list[Robot] = []

        for robot in robots:
            new_robots.append(move_robot(grid_size, robot))

        robots = new_robots

        draw(grid_size, robots, pathlib.Path("data", "d14_grids", f"{i:04}.txt"))

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
