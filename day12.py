#!/usr/bin/env python3
import re
from math import gcd

PARSE_RE = re.compile(r"<x=(.*?), y=(.*?), z=(.*?)>")

def sign(n):
    if n == 0:
        return 0
    elif n < 0:
        return -1
    else:
        return 1

class Moon:
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def __repr__(self):
        return str(self.__dict__)

def read_input():
    with open("day12.txt", "r") as fp:
        lines = fp.read().splitlines()
        moons = []
        for line in lines:
            match = PARSE_RE.match(line)
            moon = Moon([int(match.group(1)), int(match.group(2)), int(match.group(3))])
            moons.append(moon)
        return moons

def find_recurrence_dim(dim):
    moons = read_input()
    history = dict()
    i = 0
    while True:
        key = []
        for moon in moons:
            key.append((moon.position[dim], moon.velocity[dim]))
        key = tuple(key)
        if key in history:
            break
        history[key] = i
        i += 1

        for moon in moons:
            for other_moon in moons:
                if moon is other_moon:
                    continue
                moon.velocity[dim] += sign(other_moon.position[dim] - moon.position[dim])
        for moon in moons:
            moon.position[dim] += moon.velocity[dim]
    assert history[key] == 0
    return i - history[key]

def main():
    # Part 1
    moons = read_input()
    step = 0
    while step < 10:
        step += 1
        for moon in moons:
            for other_moon in moons:
                if moon is other_moon:
                    continue
                for dim in range(3):
                    moon.velocity[dim] += sign(other_moon.position[dim] - moon.position[dim])
        for moon in moons:
            for dim in range(3):
                moon.position[dim] += moon.velocity[dim]
    energy = 0
    for moon in moons:
        energy += sum(abs(p) for p in moon.position) * sum(abs(v) for v in moon.velocity)
    print(energy)

    # Part 2
    a, b, c = find_recurrence_dim(0), find_recurrence_dim(1), find_recurrence_dim(2)
    ab = a * b // gcd(a, b)
    abc = ab * c // gcd(ab, c)
    print(abc)

if __name__ == '__main__':
    main()
