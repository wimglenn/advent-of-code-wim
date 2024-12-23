"""
--- Day 7: Bridge Repair ---
https://adventofcode.com/2024/day/7
"""
from aocd import data
import operator as op
import itertools as it


def concat(n1, n2):
    return int(str(n1) + str(n2))


a = b = 0
for line in data.replace(":", "").splitlines():
    result, *ns = map(int, line.split())
    for ops in it.product((op.add, op.mul), repeat=len(ns)-1):
        val = ns[0]
        for i, f in enumerate(ops, 1):
            val = f(val, ns[i])
        if val == result:
            a += result
            b += result
            break
    else:
        for ops in it.product((op.add, op.mul, concat), repeat=len(ns) - 1):
            val = ns[0]
            for i, f in enumerate(ops, 1):
                val = f(val, ns[i])
            if val == result:
                b += result
                break

print("answer_a:", a)
print("answer_b:", b)
