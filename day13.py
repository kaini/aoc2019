#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict

def main():
    with open("day13.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)
    
    # Part 1
    screen = defaultdict(lambda: 0)
    output = run_program(defaultdict(lambda: 0, memory), iter([]))
    try:
        while True:
            x, y, v = next(output), next(output), next(output)
            screen[(x, y)] = v
    except StopIteration:
        pass
    count = 0
    for v in screen.values():
        if v == 2:
            count += 1
    print(count)

    # Part 2
    screen = defaultdict(lambda: 0)
    start_memory = defaultdict(lambda: 0, memory)
    start_memory[0] = 2
    def input2():
        while True:
            ball = None
            paddle = None
            for k, v in screen.items():
                if v == 3:
                    paddle = k
                elif v == 4:
                    ball = k
            if paddle[0] < ball[0]:
                yield 1
            elif paddle[0] > ball[0]:
                yield -1
            else:
                yield 0
    output = run_program(start_memory, input2())
    try:
        while True:
            x, y, v = next(output), next(output), next(output)
            screen[(x, y)] = v
    except StopIteration:
        pass
    print(screen[(-1, 0)])

if __name__ == '__main__':
    main()
