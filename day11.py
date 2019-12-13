#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict

def run_robot(memory, start_panels):
    panels = defaultdict(lambda: 0, start_panels)
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    direction = 0
    position = (0, 0)
    def input1():
        while True:
            yield panels[position]
    execution = run_program(defaultdict(lambda: 0, memory), input1())
    try:
        while True:
            color = next(execution)
            rotation = next(execution)
            panels[position] = color
            direction = (direction + (1 if rotation == 1 else -1)) % len(directions)
            position = (position[0] + directions[direction][0], position[1] + directions[direction][1])
    except StopIteration:
        pass
    return panels

def main():
    with open("day11.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)
    
    # Part 1
    print(len(run_robot(memory, {})))

    # Part 2
    panels = run_robot(memory, {(0, 0): 1})
    minx = min(k[0] for k in panels.keys())
    miny = min(k[1] for k in panels.keys())
    maxx = max(k[0] for k in panels.keys())
    maxy = max(k[1] for k in panels.keys())
    for y in range(miny, maxy + 1):
        for x in reversed(range(minx, maxx + 1)):
            print("#" if panels[(x, y)] else " ", end="")
        print()

if __name__ == '__main__':
    main()
