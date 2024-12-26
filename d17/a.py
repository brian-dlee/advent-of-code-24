import enum
import logging
import pathlib
import os

from aoc.puzzle_input import read_input_lines_v2
from aoc.solver import solver


class Halt(Exception):
    pass


class Opcode(enum.IntEnum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


class Computer:
    instructions: list[int]
    instruction_pointer: int
    outputs: list[int]
    register_a: int
    register_b: int
    register_c: int

    def __init__(self, register_a: int, register_b: int, register_c, instructions: list[int]):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.instructions = instructions
        self.instruction_pointer = 0
        self.outputs = []

    def read_literal_operand(self) -> int:
        location = self.instruction_pointer + 1

        if location < 0:
            raise ValueError("combo operand location cannot be negative: " + str(location))

        if location >= len(self.instructions):
            logging.debug("  out of bounds")
            raise Halt()

        operand = self.instructions[location]

        logging.debug(f"  literal operand {operand}: returning literal {operand}")

        return operand

    def read_combo_operand(self) -> int:
        location = self.instruction_pointer + 1

        if location < 0:
            raise ValueError("combo operand location cannot be negative: " + str(location))

        if location >= len(self.instructions):
            logging.debug("  out of bounds")
            raise Halt()

        match self.instructions[location]:
            case 0 | 1 | 2 | 3 as x:
                logging.debug(f"  combo operand {x}: returning literal {x}")
                return x
            case 4:
                logging.debug(f"  combo operand 4: reading register a: {self.register_a}")
                return self.register_a
            case 5:
                logging.debug(f"  combo operand 5: reading register b: {self.register_b}")
                return self.register_b
            case 6:
                logging.debug(f"  combo operand 6: reading register c: {self.register_c}")
                return self.register_c
            case x:
                raise RuntimeError("combo operand not supported: " + str(x))

    def read_next_opcode(self) -> Opcode:
        if self.instruction_pointer < 0:
            raise ValueError("invalid instruction location " + str(self.instruction_pointer))

        if self.instruction_pointer >= len(self.instructions):
            raise Halt()

        return Opcode(self.instructions[self.instruction_pointer])

    def cycle(self):
        logging.debug(f"instruction pointer is {self.instruction_pointer}")

        opcode = self.read_next_opcode()

        logging.debug(f"  opcode {opcode}")

        match opcode:
            case Opcode.adv:
                register_a = self.register_a
                operand = self.read_combo_operand()
                self.register_a = int(register_a / (2**operand))

                logging.debug(f"  adv: {register_a=} / (2^{operand=}) -> {self.register_a=}")

                self.instruction_pointer += 2
            case Opcode.bxl:
                register_b = self.register_b
                operand = self.read_literal_operand()
                self.register_b = register_b ^ operand

                logging.debug(f"  bxl: {register_b=} XOR {operand=} -> {self.register_b=}")

                self.instruction_pointer += 2
            case Opcode.bst:
                operand = self.read_combo_operand()
                self.register_b = operand % 8

                logging.debug(f"  bst: {operand=} MODULO 8 -> {self.register_b=}")

                self.instruction_pointer += 2
            case Opcode.jnz:
                if self.register_a == 0:
                    logging.debug("  jnz: register_a == 0; NOOP")

                    self.instruction_pointer += 2
                else:
                    operand = self.read_literal_operand()

                    logging.debug(f"  jnz: register_a != 0; JUMP TO {operand=}")

                    self.instruction_pointer = operand
            case Opcode.bxc:
                register_b = self.register_b
                operand = self.register_c
                ignored = self.read_literal_operand()
                self.register_b = register_b ^ operand

                logging.debug(f"  bxc: {register_b=} XOR {operand} -> {self.register_b=} ({ignored=})")

                self.instruction_pointer += 2
            case Opcode.out:
                operand = self.read_combo_operand()
                output = operand % 8

                logging.debug(f"  out: {operand=} MODULO 8 -> {output=}")

                self.outputs.append(output)
                self.instruction_pointer += 2
            case Opcode.bdv:
                register_a = self.register_a
                operand = self.read_combo_operand()
                self.register_b = int(register_a / (2**operand))

                logging.debug(f"  bdv: {register_a=} / (2^{operand=}) -> {self.register_b=}")

                self.instruction_pointer += 2
            case Opcode.cdv:
                register_a = self.register_a
                operand = self.read_combo_operand()
                self.register_c = int(register_a / (2**operand))

                logging.debug(f"  cdv: {register_a=} / (2^{operand=}) -> {self.register_c=}")

                self.instruction_pointer += 2


def wait_for_keyboard():
    if os.getenv("WAIT") == "1":
        input("(wait)")


def solve(input_file: pathlib.Path) -> str:
    register_a = 0
    register_b = 0
    register_c = 0

    instructions: list[int] = []
    for line in read_input_lines_v2(input_file):
        if line.startswith("Register A:"):
            register_a = int(line.split(": ")[-1])
        if line.startswith("Register B:"):
            register_b = int(line.split(": ")[-1])
        if line.startswith("Register C:"):
            register_c = int(line.split(": ")[-1])
        if line.startswith("Program:"):
            instructions = list(map(int, line.split(": ")[-1].split(",")))

    computer = Computer(register_a, register_b, register_c, instructions)

    logging.info(f"Starting register_a: {computer.register_a}")
    logging.info(f"Starting register_b: {computer.register_b}")
    logging.info(f"Starting register_c: {computer.register_c}")
    logging.info(f"Instructions: {len(computer.instructions)=}")
    logging.debug(f"  {computer.instructions}")

    try:
        while True:
            computer.cycle()
            wait_for_keyboard()
    except Halt:
        logging.info("HALT")

    result = ",".join(map(str, computer.outputs))

    return f"{result=}"


if __name__ == "__main__":
    solver(solve)
