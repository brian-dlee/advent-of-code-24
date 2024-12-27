import dataclasses
import logging
import pathlib

from aoc.puzzle_input import read_input_lines_v2
from aoc.solver import solver

Point = tuple[int, int]


@dataclasses.dataclass
class Node:
    position: Point
    f_score: float
    g_score: float
    previous_node: "Node | None"

    def __hash__(self) -> int:
        return hash((self.position, self.f_score, self.g_score, self.previous_node))


def pop_lowest_cost_node(node_set: set[Node]) -> Node:
    lowest_node = min(node_set, key=lambda x: x.f_score)
    node_set.remove(lowest_node)
    return lowest_node


def create_path(source_node: Node, target_node: Node) -> list[Point]:
    current_node = target_node

    path = []
    while True:
        path.insert(0, current_node.position)

        if current_node == source_node or current_node.previous_node is None:
            break

        current_node = current_node.previous_node

    return path


def get_heuristic_value(a: tuple[int, int], b: tuple[int, int]) -> float:
    ax, ay = a
    bx, by = b
    return (((bx - ax) ** 2) + ((by - ay) ** 2)) ** 0.5


def shortest_path(graph: dict[Point, list[Point]], source: Point, target: Point):
    nodes: dict[Point, Node] = {}
    nodes[source] = Node(position=source, f_score=get_heuristic_value(source, target), g_score=0, previous_node=None)

    open_set: set[Node] = set()
    open_set.add(nodes[source])

    closed_set: set[Point] = set()

    while len(open_set) > 0:
        current_node = pop_lowest_cost_node(open_set)

        if current_node.position == target:
            return create_path(nodes[source], current_node)

        closed_set.add(current_node.position)

        for neighbor in graph[current_node.position]:
            if neighbor in closed_set:
                continue

            potential_g_score = current_node.g_score + 1

            if neighbor not in nodes:
                neighbor_node = Node(
                    position=neighbor,
                    f_score=float("inf"),
                    g_score=float("inf"),
                    previous_node=None,
                )
                nodes[neighbor] = neighbor_node
            else:
                neighbor_node = nodes[neighbor]

            if potential_g_score >= neighbor_node.g_score:
                continue

            neighbor_node.previous_node = current_node
            neighbor_node.g_score = potential_g_score
            neighbor_node.f_score = potential_g_score + get_heuristic_value(neighbor, target)

            if neighbor_node not in open_set:
                open_set.add(neighbor_node)

    return None


def build_graph(grid_size: tuple[int, int], bytes_fallen: set[Point]) -> dict[Point, list[Point]]:
    w, h = grid_size

    graph: dict[Point, list[Point]] = {}

    for y in range(h):
        for x in range(w):
            if (x, y) in bytes_fallen:
                continue

            potential_positions = (
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            )

            neighbors = []

            for p in potential_positions:
                if p in bytes_fallen:
                    continue

                px, py = p

                if px < 0 or py < 0 or px >= w or py >= h:
                    continue

                neighbors.append(p)

            graph[(x, y)] = neighbors

    return graph


def draw_path(grid_size: tuple[int, int], byte_positions: set[Point], path: list[Point]) -> None:
    w, h = grid_size

    path_points = set(path)

    for y in range(h):
        for x in range(w):
            p = (x, y)
            if p in path_points:
                print("O", end="")
            elif p in byte_positions:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def solve(input_file: pathlib.Path) -> str:
    grid_size: tuple[int, int] = (71, 71)
    byte_fall_count: int = 1024

    if "sample" in input_file.name:
        grid_size = (7, 7)
        byte_fall_count = 12

    byte_positions = []
    for line in read_input_lines_v2(input_file):
        x, y = map(int, line.split(","))
        byte_positions.append((x, y))

    bytes_fallen = set()
    while len(bytes_fallen) < byte_fall_count:
        bytes_fallen.add(byte_positions.pop(0))

    print(bytes_fallen)

    draw_path(grid_size, bytes_fallen, [])

    lines = []
    for y in range(grid_size[1]):
        row = []

        for x in range(grid_size[0]):
            if (x, y) in bytes_fallen:
                row.append("#")
            else:
                row.append(".")

        lines.append(row)

    start_position = (0, 0)
    exit_position = (grid_size[0] - 1, grid_size[1] - 1)

    graph = build_graph(grid_size, bytes_fallen)

    path = shortest_path(graph, start_position, exit_position)
    if path is None:
        raise RuntimeError("no path found")

    draw_path(grid_size, bytes_fallen, path)

    result = len(path) - 1
    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
