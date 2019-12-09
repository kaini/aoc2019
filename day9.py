#!/usr/bin/env python3
from itertools import permutations
from collections import defaultdict

class Arg:
    def __init__(self, mode, addr, memory, relative_base):
        self.mode = mode
        self.addr = addr
        self.memory = memory
        self.relative_base = relative_base
    
    def get(self):
        if self.mode == 0:
            return self.memory[self.memory[self.addr]]
        elif self.mode == 1:
            return self.memory[self.addr]
        elif self.mode == 2:
            return self.memory[self.memory[self.addr] + self.relative_base]
        else:
            print("Unknown get mode", self.mode)

    def set(self, v):
        if self.mode == 0:
            self.memory[self.memory[self.addr]] = v
        elif self.mode == 1:
            print("Mode 1 set is not supported")
        elif self.mode == 2:
            self.memory[self.memory[self.addr] + self.relative_base] = v
        else:
            print("Unknown set mode", self.mode)

def decode(memory, pc, relative_base):
    return (
        Arg((memory[pc] // 10000) % 10, pc + 3, memory, relative_base),
        Arg((memory[pc] // 1000) % 10, pc + 2, memory, relative_base),
        Arg((memory[pc] // 100) % 10, pc + 1, memory, relative_base),
        memory[pc] % 100,
    )

def run_program(memory, input):
    pc = 0
    relative_base = 0
    while True:
        (arg3, arg2, arg1, op) = decode(memory, pc, relative_base)
        if op == 1:
            arg3.set(arg1.get() + arg2.get())
            pc += 4
        elif op == 2:
            arg3.set(arg1.get() * arg2.get())
            pc += 4
        elif op == 3:
            arg1.set(next(input))
            pc += 2
        elif op == 4:
            yield arg1.get()
            pc += 2
        elif op == 5:
            if arg1.get() != 0:
                pc = arg2.get()
            else:
                pc += 3
        elif op == 6:
            if arg1.get() == 0:
                pc = arg2.get()
            else:
                pc += 3
        elif op == 7:
            arg3.set(1 if arg1.get() < arg2.get() else 0)
            pc += 4
        elif op == 8:
            arg3.set(1 if arg1.get() == arg2.get() else 0)
            pc += 4
        elif op == 9:
            relative_base += arg1.get()
            pc += 2
        elif op == 99:
            break
        else:
            print("Unknown opcode", op)
            return

def main():
    with open("day9.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)
    
    # Part 1
    for output in run_program(defaultdict(lambda: 0, memory), iter([1])):
        print(output)

    # Part 2
    for output in run_program(defaultdict(lambda: 0, memory), iter([2])):
        print(output)

if __name__ == '__main__':
    main()
