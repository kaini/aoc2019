#!/usr/bin/env python3

PATTERN = [0, 1, 0, -1]
def pattern(output_i):
    while True:
        first = None
        for p in PATTERN:
            for _rep in range(output_i + 1):
                if first is None:
                    first = p
                else:
                    yield p
        yield first

def fft(input):
    prefix_sum = [0]
    for v in input:
        prefix_sum.append(prefix_sum[-1] + v)

    output = [0] * len(input)
    sign = 1
    for start_col in range(0, len(input), 2):
        for row in range(len(input)):
            col_from = (start_col + 1) * (row + 1) - 1
            col_to = (start_col + 2) * (row + 1) - 1
            if col_from >= len(input):
                break
            output[row] += sign * (prefix_sum[min(len(prefix_sum) - 1, col_to)] - prefix_sum[col_from])
        sign *= -1
    return [abs(o) % 10 for o in output]

def main():
    for row in range(100):
        piter = pattern(row)
        print("%02d: " % (row,), end="")
        for _i in range(100):
            print({-1: "-", 0: "0", +1: "+"}[next(piter)], end="")
        print()

    with open("day16.txt", "r") as fp:
        numbers = [int(s) for s in fp.read().strip()]
   
    # Part 1
    output = numbers
    for _i in range(100):
        output = fft(output)
    print("".join(str(i) for i in output)[:8])

    # Part 2
    print("You better use pypy3 ...")
    offset = int("".join(str(i) for i in numbers[:7]))
    output = numbers * 10000
    for _i in range(100):
        print(".", end="", flush=True)
        output = fft(output)
    print()
    print("".join(str(i) for i in output)[offset:offset+8])

if __name__ == '__main__':
    main()
