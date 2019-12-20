#!/usr/bin/env python3
from collections import defaultdict
from pprint import pprint

def build_map(cells):
    # Find all portals
    maxx = max(k[0] for k in cells.keys())
    maxy = max(k[1] for k in cells.keys())
    portals = defaultdict(lambda: [])
    for px in range(maxx + 1):
        for py in range(maxy + 1):
            if not ('A' <= cells[px, py] <= 'Z'):
                continue
            if cells[px, py + 1] == ".":
                dirx, diry = 0, 1
            elif cells[px, py - 1] == ".":
                dirx, diry = 0, -1
            elif cells[px + 1, py] == ".":
                dirx, diry = 1, 0
            elif cells[px - 1, py] == ".":
                dirx, diry = -1, 0
            else:
                continue
            if dirx < 0 or diry < 0:
                portal = cells[px, py] + cells[px - dirx, py - diry]
            else:
                portal = cells[px - dirx, py - diry] + cells[px, py]
            startx, starty = px + dirx, py + diry
            portals[portal].append((startx, starty))
            assert len(portals[portal]) <= 2
    
    # Use DFS to build the graph
    graph = dict() # source -> (dest, layeroffset, cost)
    for points in portals.values():
        for source in points:
            graph[source] = []
            for dest in points:
                if dest != source:
                    graph[source].append((
                        dest,
                        (-1) if (source[0] <= 2 or source[1] <= 2 or source[0] >= maxx - 2 or source[1] >= maxy - 2) else 1,
                        1
                    ))
    for points in portals.values():
        for source in points:
            frontier = [(source, 0)]
            done = set()
            while frontier:
                (atx, aty), depth = frontier.pop(0)
                if (atx, aty) in done:
                    continue
                done.add((atx, aty))
                for offx, offy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    if cells[atx+offx, aty+offy] == ".":
                        frontier.append(((atx+offx, aty+offy), depth + 1))
                if (atx, aty) != source and (atx, aty) in graph:
                    graph[source].append(((atx, aty), 0, depth))
    
    return portals, graph,

def dijkstra1(graph, start, end):
    frontier = [start]
    cost = {start: 0}
    while frontier:
        frontier.sort(key=lambda p: cost[p])
        at = frontier.pop(0)
        if at == end:
            break
        for dest, _layer_offset, edge_cost in graph[at]:
            if dest not in cost:
                cost[dest] = cost[at] + edge_cost
                frontier.append(dest)
            elif cost[at] + edge_cost < cost[dest]:
                cost[dest] = cost[at] + edge_cost
    return cost[end]

def dijkstra2(graph, start, end):
    frontier = [start]
    cost = {start: 0}
    while frontier:
        frontier.sort(key=lambda p: cost[p])
        at = frontier.pop(0)
        if at == end:
            break
        (x, y), layer = at
        for dest, layer_offset, edge_cost in graph[x, y]:
            if layer == 0 and dest not in (start[0], end[0]) and layer_offset == -1:
                continue
            dest_layer = layer + layer_offset
            if (dest, dest_layer) not in cost:
                cost[(dest, dest_layer)] = cost[at] + edge_cost
                frontier.append((dest, dest_layer))
            elif cost[at] + edge_cost < cost[(dest, dest_layer)]:
                cost[(dest, dest_layer)] = cost[at] + edge_cost
    return cost[end]

def main():
    cells = defaultdict(lambda: " ")
    with open("day20.txt", "r") as fp:
        for y, line in enumerate(fp.read().splitlines()):
            for x, c in enumerate(line):
                cells[x, y] = c

    # Part 1
    portals, graph = build_map(cells)
    cost = dijkstra1(graph, portals["AA"][0], portals["ZZ"][0])
    print(cost)

    # Part 2
    cost = dijkstra2(graph, (portals["AA"][0], 0), (portals["ZZ"][0], 0))
    print(cost)

if __name__ == '__main__':
    main()
