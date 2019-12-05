#!/usr/bin/env python3

def run_program(memory):
    pc = 0
    while True:
        op = memory[pc]
        if op == 1:
            memory[memory[pc + 3]] = memory[memory[pc + 1]] + memory[memory[pc + 2]]
            pc += 4
        elif op == 2:
            memory[memory[pc + 3]] = memory[memory[pc + 1]] * memory[memory[pc + 2]]
            pc += 4
        elif op == 99:
            break
        else:
            print("Unknown opcode")
            return

def main():
    with open("day2.txt", "r") as fp:
        memory = [int(s) for s in fp.read().split(",")]
    
    # Part 1
    memory1 = memory[:]
    memory1[1] = 12
    memory1[2] = 2
    run_program(memory1)
    print(memory1[0])

    # Part 2
    found = False
    for i in range(0, 100):
        for j in range(0, 100):
            memory2 = memory[:]
            memory2[1] = i
            memory2[2] = j
            run_program(memory2)
            if memory2[0] == 19690720:
                print(i * 100 + j)
                found = True
                break
        if found:
            break

if __name__ == '__main__':
    main()
