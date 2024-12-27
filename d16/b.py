import os
import pathlib

from aoc.puzzle_input import read_input_lines_v2
from aoc.solver import solver


Point = tuple[int, int]
Node = tuple[int, int, str]


def wait_for_keyboard() -> None:
    if os.getenv("WAIT") == "1":
        input("(wait)")


def find_char_or_raise(lines: list[str], ch: str) -> Point:
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if cell == ch:
                return (x, y)

    raise RuntimeError("unable to find char in grid: " + ch)


def flip_direction(direction: str) -> str:
    return {
        "l": "r",
        "r": "l",
        "u": "d",
        "d": "u",
    }[direction]


def get_cell(lines: list[str], point_x: int, point_y: int) -> str:
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if x == point_x and y == point_y:
                return cell

    raise RuntimeError(f"invalid cell coordinate: {(point_x, point_y)}")


def search(lines: list[str], point_x: int, point_y: int, direction: str, weight: int, visits: set[Node], depth: int):
    cell = get_cell(lines, point_x, point_y)

    if cell == "#":
        yield False, 0
        return

    if cell == "E":
        yield True, weight
        return

    visits.add((point_x, point_y, direction))
    visits.add((point_x, point_y, flip_direction(direction)))

    for next_direction in sorted(("l", "r", "u", "d"), key=lambda x: 0 if x == direction else 1):
        next_weight = weight
        next_point_x = point_x
        next_point_y = point_y

        if next_direction == direction:
            next_weight += 1
            match next_direction:
                case "r":
                    next_point_x += 1
                case "l":
                    next_point_x -= 1
                case "u":
                    next_point_y += 1
                case "d":
                    next_point_y -= 1
        else:
            next_weight += 1000

        if (next_point_x, next_point_y, next_direction) not in visits:
            yield (next_point_x, next_point_y, next_direction, next_weight, visits.copy(), depth + 1)


def build_graph(
    graph: dict[Node, dict[Node, int]], all_points: set[Node], point_x: int, point_y: int, point_d: str
) -> None:
    connections = {}

    for nd in ("r", "l", "u", "d"):
        if flip_direction(point_d) == nd:
            continue

        if nd == point_d:
            nw = 1

            match nd:
                case "l":
                    nx = point_x - 1
                    ny = point_y
                case "r":
                    nx = point_x + 1
                    ny = point_y
                case "u":
                    nx = point_x
                    ny = point_y - 1
                case "d":
                    nx = point_x
                    ny = point_y + 1
        else:
            nx = point_x
            ny = point_y
            nw = 1000

        if (nx, ny, nd) not in all_points:
            continue

        connections[(nx, ny, nd)] = nw

    graph[(point_x, point_y, point_d)] = connections


def solve(input_file: pathlib.Path) -> str:
    lines = list(read_input_lines_v2(input_file))

    start_x, start_y = find_char_or_raise(lines, "S")
    end_x, end_y = find_char_or_raise(lines, "E")

    unvisited = set()
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if cell != "#":
                for d in ("l", "r", "u", "d"):
                    unvisited.add((x, y, d))

    graph = {}
    for x, y, d in unvisited:
        build_graph(graph, unvisited, x, y, d)

    distances: dict[tuple[int, int, str], int] = {}

    for node in graph:
        distances[node] = 999999999

    distances[(start_x, start_y, "r")] = 0

    paths: dict[tuple[int, int, str], set[tuple[int, int, str]]] = {}

    for point in unvisited:
        paths[point] = set([point])

    print("progress 0.0%", end="")

    total = len(unvisited)

    while len(unvisited) > 0:
        visited_count = total - len(unvisited)

        if visited_count % 100 == 0:
            print(f"\rprogress {(visited_count / total) * 100:.1f}%", end="")

        current = min(unvisited, key=lambda p: distances[p])

        unvisited.remove(current)

        for neighbor, weight in graph[current].items():
            neighbor_distance = distances[current] + weight

            if neighbor_distance < distances[neighbor]:
                distances[neighbor] = neighbor_distance
                paths[neighbor] = paths[current].copy() | {neighbor}

            if neighbor_distance == distances[neighbor]:
                paths[neighbor].update(paths[current])
                paths[neighbor].add(neighbor)

    print("\rprogress 100.0%")

    possible_end_points = [(end_x, end_y, "u"), (end_x, end_y, "r")]
    shortest_end_point = min(possible_end_points, key=lambda x: distances[x])

    unique_points = set()
    for x, y, _ in paths[shortest_end_point]:
        unique_points.add((x, y))

    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if (x, y) in unique_points:
                print("O", end="")
            else:
                print(cell, end="")
        print()

    result = len(unique_points)
    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
