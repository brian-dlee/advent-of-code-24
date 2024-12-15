import logging
import pathlib

from aoc import grid as g
from aoc.puzzle_input import read_input_lines_v2
from aoc.solver import solver


def move_up(p: g.Point) -> g.Point:
    return p[0], g.move_up(p[1])


def move_right(p: g.Point) -> g.Point:
    return g.move_right(p[0]), p[1]


def move_down(p: g.Point) -> g.Point:
    return p[0], g.move_down(p[1])


def move_left(p: g.Point) -> g.Point:
    return g.move_left(p[0]), p[1]


def row_major(p: g.Point) -> tuple[int, int]:
    return p[1], p[0]


def calculate_perimeter(points: set[g.Point]) -> int:
    perimeter: int = 0

    for point in points:
        if move_up(point) not in points:
            perimeter += 1
        if move_right(point) not in points:
            perimeter += 1
        if move_down(point) not in points:
            perimeter += 1
        if move_left(point) not in points:
            perimeter += 1

    return perimeter


def consolidate_regions(regions: list[tuple[str, set[g.Point]]]) -> bool:
    modified = False

    for crop, region in regions:
        for point in region:
            for other_crop, other_region in regions:
                if region == other_region:
                    continue

                if other_crop != crop:
                    continue

                up, right, down, left = move_up(point), move_right(point), move_down(point), move_left(point)

                if up in other_region or right in other_region or down in other_region or left in other_region:
                    region.update(other_region)
                    other_region.intersection_update(set())
                    modified = True

    return modified


def crawl_up(grid: g.Grid, crop: str, point: g.Point) -> set[g.Point]:
    if not grid.is_in_bounds(point):
        return set()

    if grid.get(point) != crop:
        return set()

    return set([point]) & crawl_up(grid, crop, move_up(point))


def crawl_right(grid: g.Grid, crop: str, point: g.Point) -> set[g.Point]:
    if not grid.is_in_bounds(point):
        return set()

    if grid.get(point) != crop:
        return set()

    return set([point]) & crawl_right(grid, crop, move_right(point))


def crawl_down(grid: g.Grid, crop: str, point: g.Point) -> set[g.Point]:
    if not grid.is_in_bounds(point):
        return set()

    if grid.get(point) != crop:
        return set()

    return set([point]) & crawl_down(grid, crop, move_down(point))


def crawl_left(grid: g.Grid, crop: str, point: g.Point) -> set[g.Point]:
    if not grid.is_in_bounds(point):
        return set()

    if grid.get(point) != crop:
        return set()

    return set([point]) & crawl_left(grid, crop, move_left(point))


def find_crop_region(grid: g.Grid, crop: str, point: g.Point, region: set[g.Point]):
    if not grid.is_in_bounds(point):
        return

    if grid.get(point) != crop:
        return

    region.add(point)

    up, right, down, left = move_up(point), move_right(point), move_down(point), move_left(point)

    if up not in region:
        find_crop_region(grid, crop, up, region)

    if right not in region:
        find_crop_region(grid, crop, right, region)

    if down not in region:
        find_crop_region(grid, crop, down, region)

    if left not in region:
        find_crop_region(grid, crop, left, region)


def solve(input_file: pathlib.Path) -> str:
    result: int = 0

    grid = g.Grid(list(read_input_lines_v2(input_file)))

    points: set[g.Point] = set()
    for y, row in grid:
        for x, _ in row:
            points.add((x, y))

    regions: list[tuple[str, set[g.Point]]] = []
    while len(points) > 0:
        point = sorted(points, key=row_major).pop(0)
        crop = grid.get(point)

        print("Processing", point, "crop", crop)

        region: set[g.Point] = set()

        find_crop_region(grid, crop, point, region)

        for point in region:
            if point in points:
                points.remove(point)

        regions.append((crop, region))

    for i, (crop, region) in enumerate(regions):
        print("REGION", i, "CROP", crop, "AREA", len(region), "PERIMETER", calculate_perimeter(region))
        print(region)

        result += len(region) * calculate_perimeter(region)

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
