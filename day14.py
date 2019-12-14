#!/usr/bin/env python3
from collections import namedtuple, defaultdict
from math import ceil

Reaction = namedtuple("Reaction", ["materials", "result"])
Material = namedtuple("Material", ["amount", "material"])

def update_need(needs, material, amount):
    if material in needs:
        needs[material] += amount
        if needs[material] == 0:
            del needs[material]
    elif amount != 0:
        needs[material] = amount
        assert needs[material] > 0

def calc_needed_ore(reactions, needs):
    overproduction = defaultdict(lambda: 0)
    while not ("ORE" in needs and len(needs) == 1):
        new_needs = {}
        for need, amount in needs.items():
            if need == "ORE":
                update_need(new_needs, need, amount)
            else:
                amount -= overproduction[need]
                if amount < 0:
                    overproduction[need] = -amount
                else:
                    reaction = reactions[need]
                    reaction_count = ceil(amount / reaction.result.amount)
                    overproduction[need] = reaction.result.amount * reaction_count - amount
                    if overproduction[need] == 0:
                        del overproduction[need]
                    for material, amount in reaction.materials.items():
                        update_need(new_needs, material, amount * reaction_count)
        needs = new_needs
    return needs["ORE"]

def main():
    with open("day14.txt", "r") as fp:
        reactions = {}
        for line in fp.readlines():
            line = line.strip()
            if not line:
                continue
            (materials, result) = line.split(" => ")
            materials = dict((material.split()[1], int(material.split()[0])) for material in materials.split(", "))
            result = Material(int(result.split()[0]), result.split()[1])
            assert(result[1] not in reactions)
            reactions[result[1]] = Reaction(materials, result)
    
    # Part 1
    print(calc_needed_ore(reactions, {"FUEL": 1}))

    # Part 2
    max_fuel = 1
    # Starting point
    while calc_needed_ore(reactions, {"FUEL": max_fuel}) <= 1000000000000:
        max_fuel *= 2
    # Binary search
    low = 0
    high = max_fuel
    while True:
        fuel = (low + high) // 2
        needed_ore = calc_needed_ore(reactions, {"FUEL": fuel})
        if needed_ore <= 1000000000000 and calc_needed_ore(reactions, {"FUEL": fuel + 1}) > 1000000000000:
            break
        if needed_ore <= 1000000000000:
            low = fuel
        else:
            high = fuel
    print(fuel)

if __name__ == '__main__':
    main()
