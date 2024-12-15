import logging
import pathlib
import re

from aoc import grid as g
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


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    if "_sample" in input_file.name:
        grid_size = (11, 7)
    else:
        grid_size = (101, 103)

    robots: list[Robot] = []
    for px, py, vx, vy in map(read_coord_pairs, read_input_lines_v2(input_file)):
        robots.append((px, py, vx, vy))

    for _ in range(100):
        new_robots: list[Robot] = []

        for robot in robots:
            new_robots.append(move_robot(grid_size, robot))

        robots = new_robots

    w, h = grid_size

    q1, q2, q3, q4 = 0, 0, 0, 0

    for robot in robots:
        px, py, _, _ = robot

        if px < w // 2 and py < h // 2:
            q1 += 1
        elif px < w // 2 and py > h / 2:
            q2 += 1
        elif px > w / 2 and py < h // 2:
            q3 += 1
        elif px > w / 2 and py > h / 2:
            q4 += 1

    result = q1 * q2 * q3 * q4

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
