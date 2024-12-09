import logging
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines_v2
from aoc.solver import solver


Point = tuple[int, int]


def point_sub(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def point_add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def point_negate(p: Point) -> Point:
    return p[0] * -1, p[1] * -1


def solve(input_file: pathlib.Path) -> str:
    grid = g.Grid(list(read_input_lines_v2(input_file)))

    antennas: dict[str, set[Point]] = {}
    for y, row in grid:
        for x, char in row:
            if char == ".":
                continue

            antennas.setdefault(char, set())
            antennas[char].add((x, y))

    logging.debug(f"Grid: {grid}, Antennas: {antennas}")

    antinodes: dict[str, set[Point]] = {}
    for frequency in antennas.keys():
        points = list(antennas[frequency])

        for a_i in range(0, len(points) - 1):
            a = points[a_i]

            for b_i in range(a_i + 1, len(points)):
                b = points[b_i]

                logging.debug(f"Comparing {a} and {b}")

                diff = point_sub(a, b)
                antinodes.setdefault(frequency, set())
                antinodes[frequency].add(a)

                p = a
                while True:
                    p = point_add(p, diff)

                    if grid.is_in_bounds(p):
                        antinodes[frequency].add(p)
                    else:
                        break

                p = a
                while True:
                    p = point_sub(p, diff)

                    if grid.is_in_bounds(p):
                        antinodes[frequency].add(p)
                    else:
                        break

    logging.debug(f"Antinodes: {antinodes}")

    all_antinodes: set[Point] = set()
    for _, points in antinodes.items():
        for point in points:
            all_antinodes.add(point)

    result: int = len(all_antinodes)
    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
