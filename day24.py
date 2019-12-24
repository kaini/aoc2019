#!/usr/bin/env python3

def main():
    with open("day24.txt", "r") as fp:
        start_field = tuple(tuple(c for c in s) for s in fp.read().split())
    
    # Part 1
    def neighbours1(x, y):
        for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if 0 <= ny < len(start_field) and 0 <= nx < len(start_field[ny]):
                yield nx, ny
    
    def step1(field, x, y):
        bug_count = 0
        for nx, ny in neighbours1(x, y):
            if field[ny][nx] == "#":
                bug_count += 1
        if field[y][x] == "#":
            if bug_count == 1:
                return "#"
            else:
                return "."
        else:
            if bug_count == 1 or bug_count == 2:
                return "#"
            else:
                return "."

    seen = set([start_field])
    current_field = start_field
    while True:
        current_field = tuple(
            tuple(
                step1(current_field, x, y)
                for x
                in range(len(current_field[y]))
            )
            for y
            in range(len(current_field))
        )
        if current_field in seen:
            break
        seen.add(current_field)
    
    result = 0
    add = 1
    for row in current_field:
        for cell in row:
            if cell == "#":
                result += add
            add *= 2
    print(result)

    # Part 2
    def neighbours2(field, layer, x, y):
        for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if 0 <= ny < len(field[layer]) and 0 <= nx < len(field[layer][ny]):
                # Inner recursion (descend one layer)
                if nx == 2 and ny == 2 and layer > 0:
                    if nx == x-1:
                        for i in range(len(field[layer])):
                            yield layer - 1, len(field[layer][ny]) - 1, i
                    elif nx == x+1:
                        for i in range(len(field[layer])):
                            yield layer - 1, 0, i
                    elif ny == y-1:
                        for i in range(len(field[layer][ny])):
                            yield layer - 1, i, len(field[layer]) - 1
                    elif ny == y+1:
                        for i in range(len(field[layer][ny])):
                            yield layer - 1, i, 0
                    else:
                        assert False
                else:
                    # Default case (no layer change)
                    yield layer, nx, ny
            else:
                # Outer recursion (ascend one layer)
                if layer + 1 < len(field):
                    if nx == -1:
                        yield layer + 1, 1, 2
                    elif ny == -1:
                        yield layer + 1, 2, 1
                    elif ny == len(field[layer]):
                        yield layer + 1, 2, 3
                    elif nx == len(field[layer][ny]):
                        yield layer + 1, 3, 2
                    else:
                        assert False
    
    def step2(field, layer, x, y):
        if (x, y) == (2, 2):
            return "?"
        bug_count = 0
        for nlayer, nx, ny in neighbours2(field, layer, x, y):
            if field[nlayer][ny][nx] == "#":
                bug_count += 1
        if field[layer][y][x] == "#":
            if bug_count == 1:
                return "#"
            else:
                return "."
        else:
            if bug_count == 1 or bug_count == 2:
                return "#"
            else:
                return "."

    empty_layer = tuple((".",) * len(row) for row in start_field)
    current_field = (empty_layer, start_field, empty_layer)
    for _i in range(200):
        current_field = tuple(
            tuple(
                tuple(
                    step2(current_field, layer, x, y)
                    for x
                    in range(len(current_field[layer][y]))
                )
                for y
                in range(len(current_field[layer]))
            )
            for layer
            in range(len(current_field))
        )
        if current_field[0] != empty_layer:
            current_field = (empty_layer,) + current_field
        if current_field[-1] != empty_layer:
            current_field = current_field + (empty_layer,)
    print(sum(1 for layer in current_field for row in layer for c in row if c == "#"))

if __name__ == '__main__':
    main()
