#!/usr/bin/env python3

# Copied from https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Modular_integers
def galois_inverse(a, n):
    t, newt = 0, 1
    r, newr = n, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        raise Exception("a is not invertible")
    if t < 0:
        t += n
    return t

def fast_exp(value, count, neutral, plus):
    result = neutral
    for i in bin(count)[2:]:
        result = plus(result, result)
        if i == "1":
            result = plus(result, value)
    return result

def main():
    with open("day22.txt", "r") as fp:
        commands = fp.read().splitlines()
    
    # Part 1
    deck = list(range(10007))
    for command in commands:
        if not command:
            continue
        if command == "deal into new stack":
            deck.reverse()
        elif command.startswith("cut "):
            count = int(command.split()[-1])
            if count < 0:
                count += len(deck)
            deck = deck[count:] + deck[:count]
        elif command.startswith("deal with increment "):
            inc = int(command.split()[-1])
            new_deck = [0] * len(deck)
            out = 0
            for i in range(len(deck)):
                new_deck[out] = deck[i]
                out = (out + inc) % len(new_deck)
            deck = new_deck
        else:
            raise Exception("Unknown command")
    print(deck.index(2019))

    # Part 2
    cards = 119315717514047
    index = 2020
    shuffle_count = 101741582076661

    # Reverse simulate
    # All (reverse) shuffle operations are linear in the Galois Field GF(cards).
    # Therefore I can summarize the whole (reverse) shuffle algorithm to ax+b.
    a = 1
    b = 0
    for command in reversed(commands):
        if not command:
            continue
        if command == "deal into new stack":
            # -x - 1
            a = (-a) % cards
            b = (-b - 1) % cards
        elif command.startswith("cut "):
            cut = int(command.split()[-1])
            # x + cut
            b = (b + cut) % cards
        elif command.startswith("deal with increment "):
            inc = int(command.split()[-1])
            # inc and cards have to be relative prime to each other,
            # otherwise not each index would be reached.
            # Therefore, inc is a generator in the field of cards (Galois Field).
            #
            # I want to solve
            #     x * inc = index (mod cards) with gcd(inc, index) = 1.
            # This requires a division in a Galois Field
            #     index / inc = x (mod cards)
            #     index * inc^-1 = x (mod cards)
            inv = galois_inverse(inc, cards)
            a = (a * inv) % cards
            b = (b * inv) % cards
        else:
            raise Exception("Unknown command")
    print(a, "* x", "+", b)

    # Use the fast-exponentiation algorithm to apply the transformation many times.
    # To combine ax+b with cx+d one has to insert the first into the second:
    #     c(ax+b)+d = acx + bc+d
    a, b = fast_exp((a, b), shuffle_count, (1, 0), lambda a, b: ((a[0] * b[0]) % cards, (a[1] * b[0] + b[1]) % cards))
    print(a, "* x", "+", b)
    print((a * index + b) % cards)

if __name__ == '__main__':
    main()
