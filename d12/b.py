import pathlib
import string

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


def col_major(p: g.Point) -> tuple[int, int]:
    return p[0], p[1]


def row_major(p: g.Point) -> tuple[int, int]:
    return p[1], p[0]


def print_edges(size: g.Point, points: set[g.Point], edges: list[set[g.Point]]):
    min_h, max_h = 999999999, -1
    min_v, max_v = 999999999, -1

    for x, y in points:
        min_h = min(x, min_h)
        max_h = max(x, max_h)
        min_v = min(y, min_v)
        max_v = max(y, max_v)

    for y in range(-1, size[1] + 1):
        for x in range(-1, size[0] + 1):
            edge_found = False

            for i, edge in enumerate(edges):
                if (x, y) in edge:
                    print(string.ascii_uppercase[i], end="")
                    edge_found = True
                    break

            if edge_found:
                continue

            if (x, y) in points:
                print("+", end="")
            elif 0 <= x < size[0] and 0 <= y < size[1]:
                print(".", end="")
            else:
                print(" ", end="")
        print()


def print_region(crop: str, size: g.Point, points: set[g.Point]):
    min_h, max_h = 999999999, -1
    min_v, max_v = 999999999, -1

    for x, y in points:
        min_h = min(x, min_h)
        max_h = max(x, max_h)
        min_v = min(y, min_v)
        max_v = max(y, max_v)

    for y in range(-1, size[1] + 1):
        for x in range(-1, size[0] + 1):
            if (x, y) in points:
                print(crop, end="")
            elif 0 <= x < size[0] and 0 <= y < size[1]:
                print(".", end="")
            else:
                print(" ", end="")
        print()


def find_horizontal_edges(points: set[g.Point]) -> list[set[g.Point]]:
    if len(points) == 0:
        return []

    horizontal_edge_points: set[tuple[str, g.Point]] = set()

    for point in points:
        if move_up(point) not in points:
            horizontal_edge_points.add(("u", move_up(point)))
        if move_down(point) not in points:
            horizontal_edge_points.add(("d", move_down(point)))

    horizontal_edges: list[set[g.Point]] = [set()]

    for direction, point in sorted(horizontal_edge_points, key=lambda x: (x[0], row_major(x[1]))):
        latest_edge = horizontal_edges[-1]

        if len(latest_edge) == 0:
            latest_edge.add(point)
            continue

        if (direction, move_left(point)) in latest_edge:
            latest_edge.add(point)
        else:
            horizontal_edges.append(set([point]))

    return horizontal_edges


def find_vertical_edges(points: set[g.Point]) -> list[set[g.Point]]:
    if len(points) == 0:
        return []

    vertical_edge_points: set[tuple[str, g.Point]] = set()

    for point in points:
        if move_right(point) not in points:
            vertical_edge_points.add(("r", move_right(point)))
        if move_left(point) not in points:
            vertical_edge_points.add(("l", move_left(point)))

    vertical_edges: list[set[g.Point]] = [set()]

    for direction, point in sorted(vertical_edge_points, key=lambda x: (x[0], col_major(x[1]))):
        latest_edge = vertical_edges[-1]

        if len(latest_edge) == 0:
            latest_edge.add(point)
            continue

        if (direction, move_up(point)) in latest_edge:
            latest_edge.add(point)
        else:
            vertical_edges.append(set([point]))

    return vertical_edges


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

    size = (grid.col_count(), grid.row_count())

    points: set[g.Point] = set()
    for y, row in grid:
        for x, _ in row:
            points.add((x, y))

    regions: list[tuple[str, set[g.Point]]] = []
    while len(points) > 0:
        point = sorted(points, key=row_major).pop(0)
        crop = grid.get(point)
        region: set[g.Point] = set()

        find_crop_region(grid, crop, point, region)

        for point in region:
            if point in points:
                points.remove(point)

        regions.append((crop, region))

    for i, (crop, region) in enumerate(regions):
        horizontal_edges = find_horizontal_edges(region)
        vertical_edges = find_vertical_edges(region)

        sides = len(horizontal_edges) + len(vertical_edges)

        print("REGION", i, "CROP", crop, "AREA", len(region), "SIDES", sides)

        print_region(crop, size, region)
        print("horizontal")
        print_edges(size, region, horizontal_edges)
        print("vertical")
        print_edges(size, region, vertical_edges)

        result += len(region) * sides

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
