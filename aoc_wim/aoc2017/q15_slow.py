"""
--- Day 15: Dueling Generators ---
https://adventofcode.com/2017/day/15
"""
from aocd import data
from parse import parse

# Notes:
#   - The modulo (2147483647) is a mersenne prime M31: 2 ** 31 - 1
#   - The factor for generator A (16807) is 7 ** 5 (a primitive root module M31)
#   - The factor for generator B (48271) is prime
# I don't know how to exploit these facts at all, but they're actually well-known
# examples of LCGs (https://en.wikipedia.org/wiki/Linear_congruential_generator)
#   - generator A: http://www.cplusplus.com/reference/random/minstd_rand0/
#   - generator B: http://www.cplusplus.com/reference/random/minstd_rand/
# These specific factors specify a Lehmer or Park-Miller PRNG implementation:
#   https://en.wikipedia.org/wiki/Lehmer_random_number_generator
# The factors are chosen by hand because they produce a full period generating
# function with good randomness. The original 1988 paper describing this is here:
#   https://www.firstpr.com.au/dsp/rand31/p1192-park.pdf
# Maybe some obscure bit hack here can help?
#   http://graphics.stanford.edu/~seander/bithacks.html#ModulusDivision


def duel(a, b):
    fa = 16807
    fb = 48271
    d = 0x7fffffff
    count1 = 0
    a4 = []  # a values also divisible by 4
    b8 = []  # b values also divisible by 8
    for i in range(40000000):
        a = (a * fa) % d
        b = (b * fb) % d
        a16 = a & 0xffff  # lo 16 bits
        b16 = b & 0xffff
        count1 += a16 == b16
        if not a16 & 0b11:
            a4.append(a16)
        if not b16 & 0b111:
            b8.append(b16)
    # a4 will contain well over 5 million values by now, because from 40 million
    # pseudorandom numbers approx 10 million of them should be divisible by four.
    # however b8 may still be slightly under 5 million, in which case we need to
    # generate some more values.
    while len(b8) < 5000000:
        b = (b * fb) % d
        b16 = b & 0xffff
        if not b16 & 0b111:
            b8.append(b16)
    count2 = sum(a4[i] == b8[i] for i in range(5000000))
    return count1, count2


template = "Generator A starts with {:d}\nGenerator B starts with {:d}"
a0, b0 = parse(template, data).fixed
a, b = duel(a0, b0)
print("part a:", a)
print("part b:", b)
