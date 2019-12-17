#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict
import re

PATTERN = re.compile("^[ABC,]*$")

def main():
    with open("day17.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)
    
    # Part 1
    map = [[]]
    for c in run_program(defaultdict(lambda: 0, memory), iter([])):
        c = chr(c)
        if c == "\n":
            map.append([])
        else:
            map[-1].append(c)
    while map[-1] == []:
        del map[-1]
    for y in range(len(map)):
        for x in range(len(map[y])):
            print(map[y][x], end="")
        print()
    result = 0
    for y in range(1, len(map) - 1):
        for x in range(1, len(map[0]) - 1):
            if map[y][x] == "#" and map[y-1][x] == "#" and map[y+1][x] == "#" and map[y][x+1] == "#" and map[y][x-1] == "#":
                result += x * y
    print(result)

    # Part 2
    def map_get(x, y):
        if 0 <= y and y < len(map) and 0 <= x and x < len(map[y]):
            return map[y][x]
        else:
            return "."

    # Find the robot
    rx, ry = -1, -1
    dx, dy = -1, -1
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == "<":
                dx, dy = -1, 0
                rx, ry = x, y
            elif map[y][x] == "^":
                dx, dy = 0, -1
                rx, ry = x, y
            elif map[y][x] == ">":
                dx, dy = 1, 0
                rx, ry = x, y
            elif map[y][x] == "v":
                dx, dy = 0, 1
                rx, ry = x, y

    # Follow the path
    commands = []
    while True:
        # Go ahead
        commands.append(0)
        while map_get(rx+dx, ry+dy) == "#":
            commands[-1] += 1
            rx, ry = rx+dx, ry+dy
        if commands[-1] == 0:
            del commands[-1]

        # Check for a turn
        if map_get(rx+dy, ry-dx) == "#":
            commands.append("L")
            dx, dy = dy, -dx
        elif map_get(rx-dy, ry+dx) == "#":
            commands.append("R")
            dx, dy = -dy, dx
        else:
            break
    commands = [str(command) for command in commands]

    def possible_subprograms():
        for start in range(len(commands)):
            for slen in range(1, len(commands) - start + 1):
                prog = ",".join(commands[start:start+slen])
                if len(prog) <= 20:
                    yield prog
    possible_subprograms = set(possible_subprograms())

    commands_str = ",".join(commands)
    found = False
    for a in possible_subprograms:
        for b in possible_subprograms:
            for c in possible_subprograms:
                prog_str = commands_str.replace(a, "A").replace(b, "B").replace(c, "C")
                if len(prog_str) <= 20 and PATTERN.match(prog_str):
                    found = True
                    break
            if found:
                break
        if found:
            break
    print(prog_str, a, b, c)

    def program_input():
        prog = (
            prog_str + "\n" +  # main
            a + "\n" +  # A
            b + "\n" +  # B
            c + "\n" +  # C
            "n\n"  # feed
        )
        for ch in prog:
            yield(ord(ch))
    program_memory = defaultdict(lambda: 0, memory)
    program_memory[0] = 2
    program_output = run_program(program_memory, program_input())
    for po in program_output:
        if po > 128:
            print(po)
        else:
            pass
            #print(chr(po), end="")


if __name__ == '__main__':
    main()
