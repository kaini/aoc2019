#!/usr/bin/env python3
from math import gcd, sqrt, acos, asin, pi

def visible_asteorids(src_x, src_y, map):
    result = []
    for dest_x in range(len(map)):
        for dest_y in range(len(map[dest_x])):
            if (src_y == dest_y and src_x == dest_x) or map[dest_y][dest_x] == '.':
                continue
            delta_x = dest_x - src_x
            delta_y = dest_y - src_y
            # Idea: Reduce the slope to the smallest integral slope
            # (= equivalent to fraction simplification) and go steps
            # of this slope to the target. If there is a field with
            # an asteoriod encounted on one such step, it is in the
            # way of a direct line of sight.
            g = gcd(abs(delta_x if delta_x != 0 else delta_y), abs(delta_y if delta_y != 0 else delta_x))
            delta_x //= g
            delta_y //= g
            at_x = src_x
            at_y = src_y
            while True:
                at_x += delta_x
                at_y += delta_y
                if at_x != dest_x or at_y != dest_y:
                    if map[at_y][at_x] == '#':
                        # We have an asteorid in our line of sight
                        break
                else:
                    # We are at the destination
                    result.append((dest_x, dest_y))
                    break
    return result

def main():
    with open("day10.txt", "r") as fp:
        map = [list(line.strip()) for line in fp.readlines()]
    
    # Part 1
    max_count, src_x, src_y = 0, None, None
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == '#':
                this_count = len(visible_asteorids(x, y, map))
                if this_count > max_count:
                    max_count, src_x, src_y = this_count, x, y
    print(max_count)

    # Part 2
    count = 0
    while True:
        asteorids = visible_asteorids(src_x, src_y, map)
        if len(asteorids) == 0:
            break
        def to_angle(dest_x, dest_y):
            # Normalize to point on unit circle
            xx, yy = dest_x - src_x, dest_y - src_y
            l = sqrt(xx**2 + yy**2)
            xx, yy = xx / l, yy / l
            if yy > 0:
                alpha = 2 * pi - acos(xx)
            elif yy < 0:
                alpha = acos(xx)
            elif xx == 0:
                alpha = (3/2 * pi) if yy > 0 else (pi / 2)
            elif yy == 0:
                alpha = 0 if xx > 0 else pi
            alpha -= pi / 2
            if alpha <= 0:
                alpha += 2 * pi
            return -alpha
        asteorids.sort(key=lambda a: to_angle(a[0], a[1]))
        for ax, ay in asteorids:
            count += 1
            map[ay][ax] = '.'
            if count == 200:
                print(ax * 100 + ay)
                break


if __name__ == '__main__':
    main()
