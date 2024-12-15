from dataclasses import dataclass
import logging
import pathlib
import re

from aoc import grid as g
from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


class Machine:
    button_a: g.Point
    button_b: g.Point
    prize: g.Point

    def __init__(self):
        self.button_a = (0, 0)
        self.button_b = (0, 0)
        self.prize = (0, 0)

    def __str__(self) -> str:
        return f"A {self.button_a} B {self.button_b} Prize {self.prize}"

    def __repr__(self) -> str:
        return f"Machine<{self}>"

    def get_claw_position(self, button_a_presses: int, button_b_presses: int) -> g.Point:
        return point_add(
            (self.button_a[0] * button_a_presses, self.button_a[1] * button_a_presses),
            (self.button_b[0] * button_b_presses, self.button_b[1] * button_b_presses),
        )


def extract_xy(line: str) -> g.Point:
    x, y = map(int, re.findall(r"\d+", line))
    return x, y


def is_point_equal(a: g.Point, b: g.Point) -> bool:
    return a[0] == a[1] and b[0] == b[1]


def is_point_less(a: g.Point, b: g.Point) -> bool:
    return a[0] * a[1] < b[0] * b[1]


def is_point_more(a: g.Point, b: g.Point) -> bool:
    return a[0] * a[1] < b[0] * b[1]


def point_add(a: g.Point, b: g.Point) -> g.Point:
    return a[0] + b[0], a[1] + b[1]


def point_sub(a: g.Point, b: g.Point) -> g.Point:
    return a[0] - b[0], a[1] - b[1]


def solve_machine(machine: Machine) -> int:
    for a_push_count in range(100):
        for b_push_count in range(100):
            if machine.get_claw_position(a_push_count, b_push_count) == machine.prize:
                return a_push_count * 3 + b_push_count

    return -1
    # position = (0, 0)
    # a_push_count = 0
    # b_push_count = 0

    # print(f"Prize: {machine.prize}")

    # while is_point_less(position, machine.prize):
    #     position = point_add(position, machine.button_b)
    #     b_push_count += 1
    #
    #     logging.debug(f"Push B: {position} (B Pushes: {b_push_count})")
    #
    #     if b_push_count == 100:
    #         break
    #
    # while True:
    #     if is_point_equal(position, machine.prize):
    #         break
    #
    #     if is_point_less(position, machine.prize):
    #         if a_push_count == 100:
    #             break
    #
    #         position = point_add(position, machine.button_a)
    #         a_push_count += 1
    #
    #         logging.debug(f"Push A: {position} (A Pushes: {a_push_count})")
    #
    #     if is_point_more(position, machine.prize):
    #         if b_push_count == 0:
    #             break
    #
    #         position = point_sub(position, machine.button_b)
    #         b_push_count -= 1
    #
    #         logging.debug(f"Remove B: {position} (B Pushes: {b_push_count})")
    #
    # if is_point_equal(position, machine.prize):
    #     logging.debug(f"Prize Reached: {position} (A Pushes: {a_push_count}) (B Pushes: {b_push_count})")
    #     return a_push_count * 3 + b_push_count
    # else:
    #     return -1


def solve(input_file: pathlib.Path) -> str:
    machines: list[Machine] = []
    next_machine = Machine()

    for line in read_input_lines(input_file):
        line = line.strip()

        if line.startswith("Button A:"):
            next_machine.button_a = extract_xy(line)
            continue

        if line.startswith("Button B:"):
            next_machine.button_b = extract_xy(line)
            continue

        if line.startswith("Prize:"):
            next_machine.prize = extract_xy(line)
            continue

        if not line:
            machines.append(next_machine)
            next_machine = Machine()
            continue

        raise ValueError("unhandled line: " + line)

    machines.append(next_machine)

    result: int = 0

    for machine in machines:
        tokens = solve_machine(machine)
        if tokens > -1:
            result += tokens

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
