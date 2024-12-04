from aoc import grid as g

GRID = g.Grid(["...", "...", "..."])


def _trace_search(gs: g.GridSearch) -> list[str]:
    origin_x, origin_y = gs.origin
    x, y = gs.origin

    assert gs.grid.is_in_bounds((x, y)), "origin is not in bounds"

    result: list[str] = []

    while True:
        result.append(f"{x}{y}")

        x, y = gs.step_fn(x, y)

        if not gs.grid.is_in_bounds((x, y)):
            origin_x, origin_y = gs.next_fn(origin_x, origin_y)
            x, y = origin_x, origin_y

            if not gs.grid.is_in_bounds((x, y)):
                break

    return result


def test_vertical_down_search():
    trace = _trace_search(g.GridSearch.vertical_down_search(GRID))
    assert trace == ["00", "01", "02", "10", "11", "12", "20", "21", "22"]


def test_vertical_up_search():
    trace = _trace_search(g.GridSearch.vertical_up_search(GRID))
    assert trace == ["02", "01", "00", "12", "11", "10", "22", "21", "20"]


def test_horizontal_right_search():
    trace = _trace_search(g.GridSearch.horizontal_right_search(GRID))
    assert trace == ["00", "10", "20", "01", "11", "21", "02", "12", "22"]


def test_horizontal_left_search():
    trace = _trace_search(g.GridSearch.horizontal_left_search(GRID))
    assert trace == ["20", "10", "00", "21", "11", "01", "22", "12", "02"]


def test_diagonal_ul_br_search():
    trace = _trace_search(g.GridSearch.diagonal_ul_br_search(GRID))
    assert trace == ["02", "01", "12", "00", "11", "22", "10", "21", "20"]


def test_diagonal_bl_ur_search():
    trace = _trace_search(g.GridSearch.diagonal_bl_ur_search(GRID))
    assert trace == ["22", "12", "21", "02", "11", "20", "01", "10", "00"]


def test_diagonal_ur_bl_search():
    trace = _trace_search(g.GridSearch.diagonal_ur_bl_search(GRID))
    assert trace == ["22", "21", "12", "20", "11", "02", "10", "01", "00"]


def test_diagonal_br_ul_search():
    trace = _trace_search(g.GridSearch.diagonal_br_ul_search(GRID))
    assert trace == ["02", "12", "01", "22", "11", "00", "21", "10", "20"]
