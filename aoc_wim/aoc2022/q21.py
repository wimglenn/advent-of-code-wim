"""
--- Day 21: Monkey Math ---
https://adventofcode.com/2022/day/21
"""
from aocd import data
from aoc_wim.autoparse import parsed
from collections import Counter, defaultdict, deque
d = parsed(data)
if d != data:
    print(d)
    print(f"{parsed.n_bytes} bytes/{parsed.n_lines} lines, parsed by {parsed.parser}")

# import numpy as np
# import networkx as nx
# from aoc_wim.zgrid import ZGrid
# from aoc_wim import stuff

# import logging; logging.basicConfig(level=logging.DEBUG)


m = {}
for line in data.splitlines():
    m1, rest = line.split(": ")
    if rest.isdigit():
        m[m1] = int(rest)
        continue
    a, op, b = rest.split()
    assert op in "+-/*"
    m[m1] = a, op, b


while not isinstance(m["root"], int):
    changed = False
    for mname, ops in m.items():
        if isinstance(ops, int):
            continue
        a, op, b = ops
        if isinstance(m[a], int) and isinstance(m[b], int):
            if op == "+":
                m[mname] = m[a] + m[b]
            elif op == "/":
                m[mname] = m[a] // m[b]
            elif op == "-":
                m[mname] = m[a] - m[b]
            if op == "*":
                m[mname] = m[a] * m[b]
            changed = True
            break
    if not changed:
        raise Exception


print("part a:", m["root"])


m = {}
for line in data.splitlines():
    m1, rest = line.split(": ")
    if m1 == "humn":
        continue
    if rest.isdigit():
        m[m1] = int(rest)
        continue
    a, op, b = rest.split()
    if m1 == "root":
        op = "="
    else:
        assert op in "+-/*"
    m[m1] = [a, op, b]


while True:
    changed = False
    for mname, ops in m.items():
        if isinstance(ops, int):
            continue
        a, op, b = ops
        if isinstance(m.get(a), int) and isinstance(m.get(b), int):
            if op == "+":
                m[mname] = m[a] + m[b]
            elif op == "/":
                m[mname] = m[a] // m[b]
            elif op == "-":
                m[mname] = m[a] - m[b]
            if op == "*":
                m[mname] = m[a] * m[b]
            changed = True
            break
    if not changed:
        break


def fill_vals(r):
    changed = False
    for i in range(len(r)):
        if isinstance(r[i], list):
            changed = fill_vals(r[i])
        elif r[i] in m:
            r[i] = m.pop(r[i])
            changed = True
    return changed


changed = True
while changed:
    changed = fill_vals(m["root"])

import json
eq = json.dumps(m["root"]).replace("[", "(").replace("]", ")").replace(", ", "").replace('"', "").replace("=", "==")
print(eq)

import sympy
humn = sympy.Symbol("humn")
sympy.solve(eq)

print("part b:", )
