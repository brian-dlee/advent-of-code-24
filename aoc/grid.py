import dataclasses
import typing


Point = tuple[int, int]
CoordFn = typing.Callable[[int, int], Point]
Segment = list[Point]


def move_up(y: int) -> int:
    return y - 1


def move_down(y: int) -> int:
    return y + 1


def move_left(x: int) -> int:
    return x - 1


def move_right(x: int) -> int:
    return x + 1


def move_up_and_right(x: int, y: int) -> Point:
    return x + 1, y - 1


def move_up_and_left(x: int, y: int) -> Point:
    return x - 1, y + 1


def move_down_and_right(x: int, y: int) -> Point:
    return x + 1, y + 1


def move_down_and_left(x: int, y: int) -> Point:
    return x - 1, y + 1


def point_add(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def translate_left(point: Point) -> Point:
    return move_left(point[0]), point[1]


def translate_right(point: Point) -> Point:
    return move_right(point[0]), point[1]


@dataclasses.dataclass
class Grid:
    __rows: list[str]

    def __init__(self, rows: list[str]):
        self.__rows = rows

    def __iter__(self):
        for y, row in enumerate(self.__rows):
            yield y, enumerate(row)

    def copy(self) -> "Grid":
        return Grid(self.__rows.copy())

    def col_count(self) -> int:
        return len(self.__rows[0])

    def row_count(self) -> int:
        return len(self.__rows)

    def border_top(self) -> int:
        return 0

    def border_bottom(self) -> int:
        return len(self.__rows) - 1

    def border_left(self) -> int:
        return 0

    def border_right(self) -> int:
        return len(self.__rows[0]) - 1

    def corner_upper_right(self) -> Point:
        return self.border_right(), self.border_top()

    def corner_upper_left(self) -> Point:
        return self.border_left(), self.border_top()

    def corner_lower_right(self) -> Point:
        return self.border_right(), self.border_bottom()

    def corner_lower_left(self) -> Point:
        return self.border_left(), self.border_bottom()

    def get(self, xy: Point) -> str:
        return self.__rows[xy[1]][xy[0]]

    def setchar(self, xy: Point, char: str) -> None:
        line = list(self.__rows[xy[1]])
        line[xy[0]] = char
        self.__rows[xy[1]] = "".join(line)

    def is_in_bounds(self, xy: Point) -> bool:
        x, y = xy
        return self.border_left() <= x <= self.border_right() and self.border_top() <= y <= self.border_bottom()


@dataclasses.dataclass
class GridSearch:
    @staticmethod
    def vertical_down_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return x, move_down(y)

        def next_fn(x: int, _: int) -> Point:
            return move_right(x), grid.border_top()

        return GridSearch(grid, grid.corner_upper_left(), step_fn, next_fn)

    @staticmethod
    def vertical_up_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return x, move_up(y)

        def next_fn(x: int, _: int) -> Point:
            return move_right(x), grid.border_bottom()

        return GridSearch(grid, grid.corner_lower_left(), step_fn, next_fn)

    @staticmethod
    def horizontal_right_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return move_right(x), y

        def next_fn(_: int, y: int) -> Point:
            return grid.border_left(), move_down(y)

        return GridSearch(grid, grid.corner_upper_left(), step_fn, next_fn)

    @staticmethod
    def horizontal_left_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return move_left(x), y

        def next_fn(_: int, y: int) -> Point:
            return grid.border_right(), move_down(y)

        return GridSearch(grid, grid.corner_upper_right(), step_fn, next_fn)

    @staticmethod
    def diagonal_ul_br_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return move_right(x), move_down(y)

        def next_fn(x: int, y: int) -> Point:
            if y == grid.border_top():
                return move_right(x), grid.border_top()
            else:
                return grid.border_left(), move_up(y)

        return GridSearch(grid, grid.corner_lower_left(), step_fn, next_fn)

    @staticmethod
    def diagonal_bl_ur_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return move_right(x), move_up(y)

        def next_fn(x: int, y: int) -> Point:
            if x == grid.border_left():
                return grid.border_left(), move_up(y)
            else:
                return move_left(x), grid.border_bottom()

        return GridSearch(grid, grid.corner_lower_right(), step_fn, next_fn)

    @staticmethod
    def diagonal_ur_bl_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return move_left(x), move_down(y)

        def next_fn(x: int, y: int) -> Point:
            if y == grid.border_top():
                return move_left(x), grid.border_top()
            else:
                return grid.border_right(), move_up(y)

        return GridSearch(grid, grid.corner_lower_right(), step_fn, next_fn)

    @staticmethod
    def diagonal_br_ul_search(grid: Grid):
        def step_fn(x: int, y: int) -> Point:
            return move_left(x), move_up(y)

        def next_fn(x: int, y: int) -> Point:
            if x == grid.border_right():
                return grid.border_right(), move_up(y)
            else:
                return move_right(x), grid.border_bottom()

        return GridSearch(grid, grid.corner_lower_left(), step_fn, next_fn)

    grid: Grid
    origin: Point
    step_fn: CoordFn
    next_fn: CoordFn
