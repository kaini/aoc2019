#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict

def run_ascii(memory, input):
    output_iter = run_program(defaultdict(lambda: 0, memory), (ord(c) for c in input))
    for c in output_iter:
        if c > 128:
            print(c)
        elif chr(c) == "\n":
            print()
        else:
            print(chr(c), end="")

def main():
    with open("day21.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)

    # Part 1
    # (not a or not b or not c) and d
    program = (
        "NOT A T\n" +  # T = not a
        "NOT B J\n" +  # J = not b
        "OR T J\n" +   # J = not a or not b
        "NOT C T\n" +  # T = not c
        "OR T J\n" +   # J = not a or not b or not c
        "NOT D T\n" +  # T = not d
        "NOT T T\n" +  # T = d
        "AND T J\n" +  # J = (not a or not b or not c) and d
        "WALK\n"
    )
    run_ascii(memory, program)

    # Part 2
    # (not a or not b or not c) and d and (e or h)
    program = (
        "NOT A T\n" +  # T = not a
        "NOT B J\n" +  # J = not b
        "OR T J\n" +   # J = not a or not b
        "NOT C T\n" +  # T = not c
        "OR T J\n" +   # J = not a or not b or not c
        "NOT D T\n" +  # T = not d
        "NOT T T\n" +  # T = d
        "AND T J\n" +  # J = (not a or not b or not c) and d
        "NOT H T\n" +  # T = not h
        "NOT T T\n" +  # T = h
        "OR E T\n" +   # T = e or h
        "AND T J\n" +  # J = (not a or not b or not c) and d and (e or h)
        "RUN\n"
    )
    run_ascii(memory, program)

if __name__ == '__main__':
    main()
