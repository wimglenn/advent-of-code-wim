"""
--- Day 15: Dueling Generators ---
https://adventofcode.com/2017/day/15
"""
import numba
from aocd import data
from parse import parse


@numba.jit
def duel(a, b):
    fa = 16807
    fb = 48271
    d = 0x7fffffff
    count1 = count2 = 0
    a4 = []
    b8 = []
    for i in range(40000000):
        a *= fa
        a = (a & d) + (a >> 31)  # lo bits + hi bits
        a = (a & d) + (a >> 31)
        b *= fb
        b = (b & d) + (b >> 31)
        b = (b & d) + (b >> 31)
        a16 = a & 0xffff
        b16 = b & 0xffff
        count1 += a16 == b16
        if not a16 & 0b11:
            a4.append(a16)
        if not b16 & 0b111:
            b8.append(b16)
    while len(b8) < 5000000:
        b *= fb
        b = (b & d) + (b >> 31)
        b = (b & d) + (b >> 31)
        b16 = b & 0xffff
        if not b16 & 0b111:
            b8.append(b16)
    for i in range(5000000):
        count2 += a4[i] == b8[i]
    return count1, count2


template = "Generator A starts with {:d}\nGenerator B starts with {:d}"
a0, b0 = parse(template, data).fixed
a, b = duel(a0, b0)
print("part a:", a)
print("part b:", b)
