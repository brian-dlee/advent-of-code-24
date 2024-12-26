# The pretty solution isn't working, so I need to get creative
#
# I decoded my puzzle input by hand into a python program
# now I'm searching for the possible puzzles that could give me
# the known output values


def prog(a, b, c):
    b = a % 8
    b = b ^ 5
    c = int(a / (2**b))
    b = b ^ 6
    b = b ^ c
    out = b % 8
    a = int(a / 8)
    return a, b, c, out


a = 47_792_830
b = 0
c = 0
cycle = 0
while a != 0:
    a, b, c, out = prog(a, b, c)

    print("cycle", cycle)
    print(f"{a=} {b=} {c=}")
    print(out)

    cycle += 1

# I can see that my program decreases register a by a factor of 8 each iteration
# So if I start from the end I can multiply the previous solution
# by 8 each time to get an upper and lower bound to search within

solution = [2, 4, 1, 5, 7, 5, 1, 6, 4, 3, 5, 5, 0, 3, 3, 0]


def explore_in_reverse(low_bound, high_bound, solution_instruction_index):
    expected = solution[solution_instruction_index]

    for a in range(low_bound, high_bound):
        _, _, _, out = prog(a, 0, 0)

        if out == expected:
            print(f"{solution_instruction_index}: {a=}, {out=}")

            if solution_instruction_index == 0:
                return True, a

            low_bound = a * 8
            high_bound = (a + 1) * 8

            ok, a = explore_in_reverse(low_bound, high_bound, solution_instruction_index - 1)
            if ok:
                return True, a

    return False, 0


answer = explore_in_reverse(1, 8, 15)
print("part b", answer)
