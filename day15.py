#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict

NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
CW_OF = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH,
}
CCW_OF = dict((i[1], i[0]) for i in CW_OF.items())
OFFSET_OF = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}
WALL, MOVED, MOVED_GOAL = 0, 1, 2

def read_input_queue(queue):
    i = 0
    while True:
        yield queue[i]
        i += 1

def offset(pos, offset):
    return (pos[0] + offset[0], pos[1] + offset[1])

def print_map(map):
    minx = min(k[0] for k in map.keys())
    miny = min(k[1] for k in map.keys())
    maxx = max(k[0] for k in map.keys())
    maxy = max(k[1] for k in map.keys())
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) == (0, 0):
                print("0", end="")
            else:
                print(map[(x, y)], end="")
        print()

def handle_output(map, pos, input, output):
    new_pos = offset(pos, OFFSET_OF[input])
    if output == WALL:
        map[new_pos] = "#"
        return pos
    elif output == MOVED:
        map[new_pos] = "."
        return new_pos
    elif output == MOVED_GOAL:
        map[new_pos] = "x"
        return new_pos
    else:
        raise Exception("Unknown output " + str(output))

def main():
    with open("day15.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)

    # Part 1
    #########
    map = defaultdict(lambda: " ")
    pos = (0, 0)
    map[pos] = "."
    input_queue = []
    robot = run_program(defaultdict(lambda: 0, memory), read_input_queue(input_queue))

    # 1. move up until we hit a wall
    input_queue.append(NORTH)
    output = next(robot)
    pos = handle_output(map, pos, input_queue[-1], output)

    # 2. follow the wall
    start_pos = pos
    wall_dir = NORTH
    while True:
        input_queue.append(wall_dir)
        output = next(robot)
        pos = handle_output(map, pos, input_queue[-1], output)
        if output != WALL:
            wall_dir = CCW_OF[wall_dir]
        else:
            input_queue.append(CW_OF[wall_dir])
            output = next(robot)
            pos = handle_output(map, pos, input_queue[-1], output)
            if output == WALL:
                wall_dir = input_queue[-1]
        if pos == start_pos and wall_dir == NORTH:
            break
    print_map(map)

    # 3. DFS
    done = set()
    frontier = set([(0, 0)])
    iteration = 0
    oxygen_pos = None
    while True:
        for pos in frontier:
            if map[pos] == "x":
                oxygen_pos = pos
                break
        if oxygen_pos:
            break
        iteration += 1
        new_frontier = set()
        for pos in frontier:
            new_frontier.update(offset(pos, off) for off in OFFSET_OF.values() if map[offset(pos, off)] != "#" and offset(pos, off) not in done)
        done.update(frontier)
        frontier = new_frontier
    print(iteration)

    # Part 2
    #########
    # Again just use a DFS
    done = set()
    frontier = set([oxygen_pos])
    iteration = 0
    while len(frontier) > 0:
        iteration += 1
        new_frontier = set()
        for pos in frontier:
            new_frontier.update(offset(pos, off) for off in OFFSET_OF.values() if map[offset(pos, off)] != "#" and offset(pos, off) not in done)
        done.update(frontier)
        frontier = new_frontier
    print(iteration - 1)

if __name__ == '__main__':
    main()
