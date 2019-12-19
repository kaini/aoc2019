#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict

def main():
    with open("day19.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)
    
    def has_beam(x, y):
        return next(run_program(defaultdict(lambda: 0, memory), iter([x, y]))) == 1

    # Part 1
    count = 0
    for x in range(50):
        for y in range(50):
            b = 1 if has_beam(x, y) else 0
            print(b, end="")
            count += b
        print()
    print(count)

    # Part 2
    # Walk the top border of the beam
    size = 100
    tr_x, tr_y = 20, 0
    while not (has_beam(tr_x, tr_y + size - 1) and has_beam(tr_x - size + 1, tr_y) and has_beam(tr_x - size + 1, tr_y + size - 1)):
        tr_x += 1
        while not has_beam(tr_x, tr_y):
            tr_y += 1
    print((tr_x - size + 1) * 10000 + tr_y)

if __name__ == '__main__':
    main()
