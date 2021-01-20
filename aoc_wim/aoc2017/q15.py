"""
--- Day 15: Dueling Generators ---
https://adventofcode.com/2017/day/15
"""
from aocd import data
from parse import parse

template = "Generator A starts with {:d}\nGenerator B starts with {:d}"
a0, b0 = parse(template, data).fixed

# notes:
#   the factor for generator A, 16807, is 7 ** 5
#   the factor for generator B, 48271, is prime
#   the modulo, 2147483647, is a mersenne prime: 2 ** 31 - 1


def duel(a, b):
    fa = 16807
    fb = 48271
    d = 2147483647
    count1 = 0
    a4 = []  # a values also divisible by 4
    b8 = []  # b values also divisible by 8
    for i in range(40000000):
        a = (a * fa) % d
        b = (b * fb) % d
        a16 = a & 0xFFFF
        b16 = b & 0xFFFF
        count1 += a16 == b16
        if not a16 & 0b11:
            a4.append(a16)
        if not b16 & 0b111:
            b8.append(b16)
    # a4 will contain well over 5 million values by now, because from 40 million
    # pseudorandom numbers approx 10 million of them should be divisible by four.
    # however b8 may still be slightly under 5 million and need more values generated.
    while len(b8) < 5000000:
        b = (b * fb) % d
        b16 = b & 0xFFFF
        if not b16 & 0b111:
            b8.append(b16)
    count2 = sum(a4[i] == b8[i] for i in range(5000000))
    return count1, count2


count_a, count_b = duel(a0, b0)
print("part a:", count_a)
print("part b:", count_b)
