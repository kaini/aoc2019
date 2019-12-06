#!/usr/bin/env python3

def main():
    orbits = dict()
    with open("day6.txt", "r") as fp:
        for line in fp.read().splitlines():
            center_of_mass, in_orbit = line.split(")")
            orbits[in_orbit] = center_of_mass
    
    # Part 1
    count = 0
    for o in orbits.keys():
        o_count = 0
        while o in orbits:
            o_count += 1
            o = orbits[o]
        count += o_count
    print(count)

    # Part 2
    you_parents = []
    o = "YOU"
    while o in orbits:
        o = orbits[o]
        you_parents.append(o)
    
    o = "SAN"
    steps = 0
    while o in orbits:
        o = orbits[o]
        try:
            steps += you_parents.index(o)
            break
        except ValueError:
            pass
        steps += 1
    print(steps)


if __name__ == '__main__':
    main()
