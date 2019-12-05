#!/usr/bin/env python3

def recfuel(n):
    result = 0
    n = n // 3 - 2
    while n > 0:
        result += n
        n = n // 3 - 2
    return result

def main():
    with open("day1.txt", "r") as fp:
        numbers = [int(s) for s in fp.read().split()]
    print(sum(n // 3 - 2 for n in numbers))
    print(sum(recfuel(n) for n in numbers))

if __name__ == '__main__':
    main()
