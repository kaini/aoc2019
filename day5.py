#!/usr/bin/env python3

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

def run_program(memory, input, output):
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
            arg1.set(input())
            pc += 2
        elif op == 4:
            output(arg1.get())
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
    with open("day5.txt", "r") as fp:
        memory = [int(s) for s in fp.read().split(",")]
    
    # Part 1
    def output1(v):
        if v != 0:
            print(v)
    run_program(memory[:], lambda: 1, output1)

    # Part 2
    run_program(memory[:], lambda: 5, print)

if __name__ == '__main__':
    main()
