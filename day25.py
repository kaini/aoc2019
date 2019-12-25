#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict

def main():
    with open("day25.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)
    
    # Part 1
    #
    #                               Stables -- Crew Quarters - Engineering - Corridor
    #                                                |      SCP - Arcade                 Sick Bay
    #                                                |                                   Kitchen ------ Hallway
    #           Storage --- Passages -- GWC --- Science Lab -- Holodeck ---- Warp Drive Maintenance
    #                Hot Chocolate Fountain                   Hull Breach
    #
    #
    # Holodeck: giant electromagnet (don't take this)
    # Warp Drive Maintenance: ornament
    # Kitchen: escape pod (leaves the ship)
    # Sick Bay: dark matter
    # Crew Quarters: astrolabe
    # Engineering: hologram
    # Corridor: klein bottle
    # Arcade: molten lava (don't take this)
    # GWC: candy cane
    # Passages: photons (don't take this)
    # Storage: tambourine
    last_output = "Command?"
    def brute_force_checkput(dir, items):
        for item in items:
            yield "drop " + item
        for i in range(2**len(items)):
            for bit in range(len(items)):
                if i & (1 << bit):
                    yield "take " + items[bit]
            yield dir
            if "Alert!" not in last_output:
                break
            for bit in range(len(items)):
                if i & (1 << bit):
                    yield "drop " + items[bit]
        print("NO SOLUTION FOUND!")
    def input1():
        # First take all the items in the lower half of the ship
        take_all_items = "\n".join([
            "north",
            "east", "take ornament",
            "north",
            "north", "take dark matter",
            "south",
            "south",
            "west",
            "west",
            "west", "take candy cane",
            "west",
            "west", "take tambourine",
            "east",
            "east",
            "east",
            "north", "take astrolabe",
            "east", "take hologram",
            "east", "take klein bottle",
            "west",
            "south",
            "west",
        ]) + "\n"
        for c in take_all_items:
            yield ord(c)
        items = ["ornament", "dark matter", "candy cane", "tambourine", "astrolabe", "hologram", "klein bottle"]

        # Try to pass the first Security Checkpoint (SCP)
        for command in brute_force_checkput("north", items):
            for c in command:
                yield ord(c)
            yield(ord("\n"))

        while True:
            line = input()
            line = line.strip() + "\n"
            for c in line:
                yield ord(c)
    for c in run_program(defaultdict(lambda: 0, memory), input1()):
        if chr(c) == "\n":
            print()
        else:
            print(chr(c), end="")
        last_output += chr(c)
        if last_output.endswith("Command?"):
            last_output = last_output[last_output.index("Command?") + 8:]

if __name__ == '__main__':
    main()
