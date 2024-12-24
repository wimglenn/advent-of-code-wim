"""
--- Day 24: Crossed Wires ---
https://adventofcode.com/2024/day/24
"""
from aocd import data
from collections import deque
import operator


def parse(data):
    wires = {}
    ops = deque([])
    op_map = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}
    for line in data.splitlines():
        match line.split():
            case wire, val:
                wires[wire.rstrip(":")] = int(val)
            case w0, op, w1, _, w2:
                ops.appendleft([op_map[op], w0, w1, w2])
    return wires, ops


def get_val(wires, name="z"):
    return sum(bit << int(w[1:]) for w, bit in wires.items() if w.startswith(name))


def compute(wires, ops):
    while ops:
        operator, *args, dest = ops.popleft()
        if any(o not in wires for o in args):
            ops.append([operator, *args, dest])  # procrastinate
            continue
        operands = [wires[arg] for arg in args]
        wires[dest] = operator(*operands)
    return get_val(wires)


wires, ops = parse(data)
a = compute(wires, ops)
print("answer_a:", a)


def swap_outputs(out1, out2, instructions):
    [i1] = [x for x in instructions if x[-1] == out1]
    [i2] = [x for x in instructions if x[-1] == out2]
    i1[-1], i2[-1] = out2, out1


swap = [
    ("z29", "gbs"),
    ("z22", "hwq"),
    ("z08", "thm"),
    ("wrm", "wss"),
]
wires, ops = parse(data)
x = get_val(wires, name="x")
y = get_val(wires, name="y")
for out1, out2 in swap:
    swap_outputs(out1, out2, ops)
z = compute(wires, ops)
if x + y == z:
    print("answer_b:", ",".join(sorted(sum(swap, ()))))
