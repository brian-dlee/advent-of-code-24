import logging
import pathlib
import typing

from aoc.puzzle_input import read_input_lines
from aoc.solver import solver


Equation = tuple[int, list[int]]


def translate_bit(bit: str) -> str:
    match bit:
        case "0":
            return "+"
        case "1":
            return "*"
        case _:
            raise ValueError("unexpected bit " + bit)


def bitmap_to_operators(value: int, operator_count: int) -> list[str]:
    return [translate_bit(b) for b in bitmap_str(value, operator_count)]


def bitmap_str(value: int, length: int) -> str:
    result = bin(value)[2:]

    if length < len(result):
        raise ValueError("binary string is longer than expected")

    if length > len(result):
        return ((length - len(result)) * "0") + result
    else:
        return result


def is_valid(test_value: int, operands: list[int], operators: list[str]) -> bool:
    left_operand = operands[0]

    trace = [test_value, "=", left_operand]

    for i in range(1, len(operands)):
        right_operand = operands[i]
        operator = operators[i - 1]

        trace += [operator, right_operand]

        match operator:
            case "+":
                left_operand = left_operand + right_operand
            case "*":
                left_operand = left_operand * right_operand

    y = left_operand == test_value

    logging.debug(f"is_valid? {y}: {left_operand} -> {' '.join(map(str, trace))}")

    return y


def iter_equation(equation: Equation) -> typing.Generator[tuple[int, list[int], list[str]], None, None]:
    test_value, operands = equation
    logging.debug(f"{test_value} = {operands}")

    operands_bitmap = int("0" * (len(operands) - 1), base=2)
    operator_count = len(operands) - 1
    iter_count = 2 ** (len(operands) - 1)

    logging.debug(f"{bitmap_str(operands_bitmap, operator_count)=} {operator_count=} {iter_count=}")

    for i in range(iter_count):
        yield test_value, operands, bitmap_to_operators(operands_bitmap + i, operator_count)


def solve(input_file: pathlib.Path) -> str:
    equations: list[Equation] = []

    for line in read_input_lines(input_file):
        line = line.strip()

        equation_output, equation_operands = line.split(": ")
        equations.append((int(equation_output), list(map(int, equation_operands.split(" ")))))

    result: int = 0

    for equation in equations:
        for test_value, operands, operators in iter_equation(equation):
            if is_valid(test_value, operands, operators):
                result += test_value
                break

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
