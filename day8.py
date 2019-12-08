#!/usr/bin/env python3

W = 25
H = 6
OUTPUT = {
    "0": " ",
    "1": "#",
    "2": "?",
}

def main():
    with open("day8.txt", "r") as fp:
        data = fp.read().strip()
    
    # Part 1
    layers = []
    for layer in range(len(data) // (W*H)):
        layers.append(data[W*H*layer:W*H*(layer+1)])
    chosen_layer = min(layers, key=lambda l: l.count('0'))
    print(chosen_layer.count('1') * chosen_layer.count('2'))

    # Part 2
    result = ['2'] * (W * H)
    for i in range(len(result)):
        for layer in layers:
            result[i] = layer[i]
            if result[i] != '2':
                break
    for y in range(H):
        for x in range(W):
            print(OUTPUT[result[y * W + x]], end="")
        print()

if __name__ == '__main__':
    main()

