import pytest

from d17.a import Computer, Halt, Opcode


GARBAGE = 999999


def test_literal_operand():
    computer = Computer(register_a=GARBAGE, register_b=GARBAGE, register_c=GARBAGE, instructions=[])

    computer.instructions = [0, 0]
    assert computer.read_literal_operand() == 0
    computer.instructions = [0, 1]
    assert computer.read_literal_operand() == 1
    computer.instructions = [0, 2]
    assert computer.read_literal_operand() == 2
    computer.instructions = [0, 3]
    assert computer.read_literal_operand() == 3
    computer.instructions = [0, 4]
    assert computer.read_literal_operand() == 4
    computer.instructions = [0, 5]
    assert computer.read_literal_operand() == 5
    computer.instructions = [0, 6]
    assert computer.read_literal_operand() == 6
    computer.instructions = [0, 7]
    assert computer.read_literal_operand() == 7


def test_combo_operand():
    computer = Computer(register_a=100, register_b=200, register_c=300, instructions=[])

    computer.instructions = [0, 0]
    assert computer.read_combo_operand() == 0
    computer.instructions = [0, 1]
    assert computer.read_combo_operand() == 1
    computer.instructions = [0, 2]
    assert computer.read_combo_operand() == 2
    computer.instructions = [0, 3]
    assert computer.read_combo_operand() == 3
    computer.instructions = [0, 4]
    assert computer.read_combo_operand() == computer.register_a
    computer.instructions = [0, 5]
    assert computer.read_combo_operand() == computer.register_b
    computer.instructions = [0, 6]
    assert computer.read_combo_operand() == computer.register_c
    computer.instructions = [0, 7]
    with pytest.raises(RuntimeError):
        computer.read_combo_operand()


def test_adv():
    computer = Computer(register_a=81, register_b=GARBAGE, register_c=GARBAGE, instructions=[Opcode.adv, 3])

    computer.cycle()

    assert computer.register_a == 10
    assert computer.register_b == GARBAGE
    assert computer.register_c == GARBAGE
    assert computer.outputs == []
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()


def test_bxl():
    computer = Computer(register_a=GARBAGE, register_b=52, register_c=GARBAGE, instructions=[Opcode.bxl, 7])

    computer.cycle()

    assert computer.register_a == GARBAGE
    assert computer.register_b == 52 ^ 7
    assert computer.register_c == GARBAGE
    assert computer.outputs == []
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()


def test_bst():
    computer = Computer(register_a=GARBAGE, register_b=52, register_c=GARBAGE, instructions=[Opcode.bst, 5])

    computer.cycle()

    assert computer.register_a == GARBAGE
    assert computer.register_b == 52 % 8
    assert computer.register_c == GARBAGE
    assert computer.outputs == []
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()


def test_jnz_noop():
    computer = Computer(register_a=0, register_b=GARBAGE, register_c=GARBAGE, instructions=[Opcode.jnz, 3])

    computer.cycle()

    assert computer.register_a == 0
    assert computer.register_b == GARBAGE
    assert computer.register_c == GARBAGE
    assert computer.outputs == []
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()


def test_jnz_jump():
    computer = Computer(register_a=1, register_b=GARBAGE, register_c=GARBAGE, instructions=[Opcode.jnz, 5])

    computer.cycle()

    assert computer.register_a == 1
    assert computer.register_b == GARBAGE
    assert computer.register_c == GARBAGE
    assert computer.outputs == []
    assert computer.instruction_pointer == 5

    with pytest.raises(Halt):
        computer.cycle()


def test_bxc():
    computer = Computer(register_a=GARBAGE, register_b=25, register_c=32, instructions=[Opcode.bxc, 7])

    computer.cycle()

    assert computer.register_a == GARBAGE
    assert computer.register_b == 25 ^ 32
    assert computer.register_c == 32
    assert computer.outputs == []
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()


def test_bxc_read_ignore():
    computer = Computer(register_a=GARBAGE, register_b=GARBAGE, register_c=GARBAGE, instructions=[Opcode.bxc])

    with pytest.raises(Halt):
        computer.cycle()


def test_out():
    computer = Computer(register_a=GARBAGE, register_b=GARBAGE, register_c=19, instructions=[Opcode.out, 6])

    computer.cycle()

    assert computer.register_a == GARBAGE
    assert computer.register_b == GARBAGE
    assert computer.register_c == 19
    assert computer.outputs == [19 % 8]
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()


def test_bdv():
    computer = Computer(register_a=150, register_b=6, register_c=GARBAGE, instructions=[Opcode.bdv, 5])

    computer.cycle()

    assert computer.register_a == 150
    assert computer.register_b == int(150 / (2**6))
    assert computer.register_c == GARBAGE
    assert computer.outputs == []
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()


def test_cdv():
    computer = Computer(register_a=17, register_b=GARBAGE, register_c=GARBAGE, instructions=[Opcode.cdv, 4])

    computer.cycle()

    assert computer.register_a == 17
    assert computer.register_b == GARBAGE
    assert computer.register_c == int(17 / (2**17))
    assert computer.outputs == []
    assert computer.instruction_pointer == 2

    with pytest.raises(Halt):
        computer.cycle()
