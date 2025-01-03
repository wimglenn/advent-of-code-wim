"""
--- Day 24: Crossed Wires ---
https://adventofcode.com/2024/day/24
"""
import itertools as it
from collections import deque

from aocd import data
from aocd import extra


def parse(data):
    wires = {}
    ops = []
    for line in data.splitlines():
        match line.split():
            case wire, val:
                wires[wire.rstrip(":")] = int(val)
            case i0, op, i1, _, out:
                i0, i1 = sorted([i0, i1])
                ops.append([i0, op, i1, out])
    return wires, ops


def get_val(wires, name="z"):
    return sum(bit << int(w[1:]) for w, bit in wires.items() if w[0] == name)


def compute(wires, ops):
    q = deque(ops)
    while q:
        L = i0, op, i1, out = q.popleft()
        if i0 not in wires or i1 not in wires:
            q.append(L)  # procrastinate
            continue
        x, y = wires[i0], wires[i1]
        wires[out] = x & y if op == "AND" else x | y if op == "OR" else x ^ y
    return get_val(wires)


wires, ops = parse(data)
a = compute(wires, ops)
print("answer_a:", a)

swapped = []
n_swapped = 2 * extra.get("n_swapped_pairs", 4)
zs = sorted([w for w in wires if w[0] == "z"])
if extra.get("operation") == "bitwise_and":
    d0 = {}
    for z in zs:
        d0[z.replace("z", "x")] = d0[z.replace("z", "y")] = 0
    for z in zs:
        w = d0.copy()
        w[z.replace("z", "x")] = w[z.replace("z", "y")] = 1
        z_out = compute(w, ops)
        [i] = [i for i in range(len(zs)) if 2**i == z_out]
        if int(z[1:]) != i:
            swapped += [z, f"z{i:02d}"]
        if len(swapped) == n_swapped:
            break

# https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder
or_operands = {i0 for i0, op, i1, out in ops if op == "OR"}
or_operands |= {i1 for i0, op, i1, out in ops if op == "OR"}
and_operands = {i0 for i0, op, i1, out in ops if op == "AND"}
and_operands |= {i1 for i0, op, i1, out in ops if op == "AND"}
for i0, op, i1, out in ops:
    if len(swapped) == n_swapped:
        break
    if i0 == "x00" and i1 == "y00":
        continue
    elif out[0] == "z" and out != zs[-1] and op != "XOR":
        swapped.append(out)
    elif out[0] != "z" and i0[0] != "x" and i1[0] != "y" and op == "XOR":
        swapped.append(out)
    elif i0[0] == "x" and i1[0] == "y" and op == "AND" and out not in or_operands:
        swapped.append(out)
    elif i0[0] == "x" and i1[0] == "y" and op == "XOR" and out not in and_operands:
        swapped.append(out)
print("answer_b:", ",".join(sorted(swapped)))
