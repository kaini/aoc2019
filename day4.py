#!/usr/bin/env python3
import re

INPUT = "124075-580769"
FROM, TO = [int(s) for s in INPUT.split("-")]

DOUBLEDIGIT1 = re.compile(r"^.*(00|11|22|33|44|55|66|77|88|99).*$")
DOUBLEDIGIT2 = re.compile(r"^.*(" + "|".join(f"((^|[^{d}]){d}{d}($|[^{d}]))" for d in "0123456789") + r").*$")
NODECREASE = re.compile(r"^0*1*2*3*4*5*6*7*8*9*$")

def is_valid1(p):
    return DOUBLEDIGIT1.match(p) and NODECREASE.match(p)

def is_valid2(p):
    return DOUBLEDIGIT2.match(p) and NODECREASE.match(p)

def main():
    count1 = 0
    count2 = 0
    for password in range(FROM, TO + 1):
        if is_valid1(str(password)):
            count1 += 1
        if is_valid2(str(password)):
            count2 += 1
    print(count1)
    print(count2)

if __name__ == '__main__':
    main()
