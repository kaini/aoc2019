#!/usr/bin/env python3
from pprint import pprint

def tset(tpl, idx, newval):
    return tuple((newval if i == idx else val) for i, val in enumerate(tpl))

def build_dists(map):
    dists = dict()
    for source in map.keys():
        if ("a" <= map[source] and map[source] <= "z") or map[source] in "@1234":
            dists[map[source]] = dict()
            frontier = [(source, 0, frozenset())]
            done = set()
            while frontier:
                pos, depth, doors = frontier.pop(0)
                if pos in done:
                    continue
                done.add(pos)

                if map[pos] != "#":
                    if "a" <= map[pos] and map[pos] <= "z":
                        dists[map[source]][map[pos]] = (depth, doors)
                    
                    if "A" <= map[pos] and map[pos] <= "Z":
                        new_doors = doors.union([map[pos].lower()])
                    else:
                        new_doors = doors
                    
                    frontier.append(((pos[0] + 1, pos[1]), depth + 1, new_doors))
                    frontier.append(((pos[0] - 1, pos[1]), depth + 1, new_doors))
                    frontier.append(((pos[0], pos[1] + 1), depth + 1, new_doors))
                    frontier.append(((pos[0], pos[1] - 1), depth + 1, new_doors))
    return dists

def search(dists, start_nodes):
    best_cost = 99999999
    best_subcost = dict()

    def dfs(current_nodes, current_cost, current_keys):
        nonlocal best_cost, best_subcost

        if (current_nodes, current_keys) in best_subcost and best_subcost[current_nodes, current_keys] <= current_cost:
            return  # already explored (in a cheaper way)
        best_subcost[current_nodes, current_keys] = current_cost

        if current_cost >= best_cost:
            return  # already too expensive

        if len(current_keys) == len(dists) - len(start_nodes):
            print(best_cost, "->", current_cost)
            best_cost = current_cost  # all keys found
            return

        for node_idx in range(len(current_nodes)):
            for dest, (cost, needed_keys) in sorted(dists[current_nodes[node_idx]].items(), key=lambda e: e[1][0]):
                if dest in current_keys:
                    continue  # already visited
                if len(needed_keys - current_keys) > 0:
                    continue  # cannot be reached yet
                dfs(tset(current_nodes, node_idx, dest), current_cost + cost, current_keys.union([dest]))
    
    dfs(start_nodes, 0, frozenset())
    return best_cost

def main():
    map = dict()
    start = None
    with open("day18.txt", "r") as fp:
        for y, line in enumerate(fp.readlines()):
            for x, cell in enumerate(line.strip()):
                map[x, y] = cell
                if cell == "@":
                    start = x, y
    
    # Part 1
    dists = build_dists(map)
    #pprint(dists)
    print(search(dists, ("@",)))
    print()

    # Part 2
    map[start[0] - 1, start[1] - 1] = "1"
    map[start[0] - 1, start[1] + 0] = "#"
    map[start[0] - 1, start[1] + 1] = "2"
    map[start[0] + 0, start[1] - 1] = "#"
    map[start[0] + 0, start[1] + 0] = "#"
    map[start[0] + 0, start[1] + 1] = "#"
    map[start[0] + 1, start[1] - 1] = "3"
    map[start[0] + 1, start[1] + 0] = "#"
    map[start[0] + 1, start[1] + 1] = "4"
    dists = build_dists(map)
    #pprint(dists)
    print(search(dists, ("1", "2", "3", "4")))


if __name__ == '__main__':
    main()
