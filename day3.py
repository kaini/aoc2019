#!/usr/bin/env python3

def mdist(pos):
    return abs(pos[0]) + abs(pos[1])

def walk_path(path):
    x, y, steps = 0, 0, 0
    positions = dict()
    positions[(x, y)] = steps
    for command in path.split(","):
        dir, amount = command[0], int(command[1:])
        for _i in range(amount):
            if dir == "L":
                x -= 1
            elif dir == "R":
                x += 1
            elif dir == "D":
                y -= 1
            elif dir == "U":
                y += 1
            else:
                print("Unknown direction")
            steps += 1
            if (x, y) not in positions:
                positions[(x, y)] = steps
    return positions

def main():
    with open("day3.txt", "r") as fp:
        path1, path2 = fp.read().splitlines()

    pos1 = walk_path(path1)
    pos2 = walk_path(path2)

    # Part 1
    pos = set(pos1.keys()).intersection(set(pos2.keys()))
    pos.remove((0, 0))
    print(mdist(min(pos, key=mdist)))

    # Part 2
    result = min(pos, key=lambda p: pos1[p] + pos2[p])
    print(pos1[result] + pos2[result])

if __name__ == '__main__':
    main()
