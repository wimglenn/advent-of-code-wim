"""
--- Day 24: Crossed Wires ---
https://adventofcode.com/2024/day/24
"""
from collections import Counter
from collections import deque

from aocd import data
from aocd import extra

from aoc_wim.stuff import unique_groupings


def parsed(data, swapped_pairs=()):
    swap_map = dict(swapped_pairs)
    swap_map.update({v: k for k, v in swap_map.items()})
    wires = {}
    ops = []
    for line in data.splitlines():
        match line.split():
            case wire, val:
                wires[wire.rstrip(":")] = int(val)
            case i0, op, i1, _, out:
                i0, i1 = sorted([i0, i1])
                ops.append([i0, op, i1, swap_map.get(out, out)])
    return wires, ops


def get_val(wires, name="z"):
    return sum(bit << int(w[1:]) for w, bit in wires.items() if w[0] == name)


def compute(wires, ops):
    q = deque(ops)
    no_signal = Counter()
    while q:
        L = i0, op, i1, out = q.popleft()
        if i0 not in wires or i1 not in wires:
            no_signal[i0] += i0 not in wires
            no_signal[i1] += i1 not in wires
            if no_signal[i0] > 100 or no_signal[i1] > 100:
                return None
            q.append(L)  # procrastinate
            continue
        x, y = wires[i0], wires[i1]
        wires[out] = x & y if op == "AND" else x | y if op == "OR" else x ^ y
    return get_val(wires)


wires, ops = parsed(data)
x = get_val(wires, name="x")
y = get_val(wires, name="y")
z_expected = x + y
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
    z_expected = x & y

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

candidates = []

for swaps in unique_groupings(swapped, 2):
    wires, ops = parsed(data, swaps)
    if compute(wires, ops) == z_expected:
        for s1, s2 in sorted(swaps):
            print(s1, "<->", s2)
        candidates.append(swaps)
        print("answer_b:", ",".join(sorted(swapped)))


def add(x, y, swaps):
    assert 0 <= x < 2**45
    assert 0 <= y < 2**45
    wires = []
    for i, bit in enumerate(format(x, "045b")[::-1]):
        wires.append(f"x{i:02d}: {bit}")
    for i, bit in enumerate(format(y, "045b")[::-1]):
        wires.append(f"y{i:02d}: {bit}")
    patched_data = "\n".join(wires) + "\n\n" + data.split("\n\n")[1]
    wires, ops = parsed(patched_data, swaps)
    z = compute(wires, ops)
    print(f"x: {x:046b}")
    print(f"y: {y:046b}")
    print(f"z: {z:046b}")
    print(x + y == z)
    return z
