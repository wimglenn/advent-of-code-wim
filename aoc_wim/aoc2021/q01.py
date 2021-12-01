"""
--- Day 1: Sonar Sweep ---
https://adventofcode.com/2021/day/1
"""
from aocd import data

ns = [int(n) for n in data.split()]
a = sum(n2 > n1 for n1, n2 in zip(ns, ns[1:]))
n3s = [sum(n3) for n3 in zip(ns, ns[1:], ns[2:])]
b = sum(n2 > n1 for n1, n2 in zip(n3s, n3s[1:]))

print("part a:", a)
print("part b:", b)
