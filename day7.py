#!/usr/bin/env python3
from itertools import permutations

class Arg:
    def __init__(self, mode, addr, memory):
        self.mode = mode
        self.addr = addr
        self.memory = memory
    
    def get(self):
        if self.mode == 0:
            return self.memory[self.memory[self.addr]]
        elif self.mode == 1:
            return self.memory[self.addr]
        else:
            print("Unknown get mode", self.mode)

    def set(self, v):
        if self.mode == 0:
            self.memory[self.memory[self.addr]] = v
        elif self.mode == 1:
            print("Mode 1 set is not supported")
        else:
            print("Unknown set mode", self.mode)

def decode(memory, pc):
    return (
        Arg((memory[pc] // 10000) % 10, pc + 3, memory),
        Arg((memory[pc] // 1000) % 10, pc + 2, memory),
        Arg((memory[pc] // 100) % 10, pc + 1, memory),
        memory[pc] % 100,
    )

def run_program(memory, input):
    pc = 0
    while True:
        (arg3, arg2, arg1, op) = decode(memory, pc)
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
        elif op == 99:
            break
        else:
            print("Unknown opcode", op)
            return

def main():
    with open("day7.txt", "r") as fp:
        memory = [int(s) for s in fp.read().split(",")]
    
    # Part 1
    max_output = 0
    for (a, b, c, d, e) in permutations(range(0, 5)):
        out_a = next(run_program(memory[:], iter([a, 0])))
        out_b = next(run_program(memory[:], iter([b, out_a])))
        out_c = next(run_program(memory[:], iter([c, out_b])))
        out_d = next(run_program(memory[:], iter([d, out_c])))
        out_e = next(run_program(memory[:], iter([e, out_d])))
        max_output = max(max_output, out_e)
    print(max_output)

    # Part 2
    value = 0
    max_output = 0
    def input2(parameters):
        for p in parameters:
            yield p
            yield value
        while True:
            yield value
    for parameters in permutations([5, 6, 7, 8, 9]):
        infn = input2(parameters)
        programs = [run_program(memory[:], infn) for p in parameters]
        try:
            while True:
                for program in programs:
                    value = next(program)
        except StopIteration:
            pass
        max_output = max(max_output, value)
        value = 0
    print(max_output)
        

if __name__ == '__main__':
    main()
