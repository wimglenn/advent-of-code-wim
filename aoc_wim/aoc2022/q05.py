"""
--- Day 5: Supply Stacks ---
https://adventofcode.com/2022/day/5
"""
from aocd import data
from parse import parse

crates, instructions = data.split("\n\n")
cols0 = {}
for *row, last in zip(*crates.split("\n")):
    if last.isdigit():
        cols0[int(last)] = "".join(x for x in row if x.isupper())

moves = []
for line in instructions.splitlines():
    n, p0, p1 = parse("move {:d} from {:d} to {:d}", line).fixed
    moves.append((n, p0, p1))

for part in "ab":
    step = -1 if part == "a" else None
    cols = cols0.copy()
    for n, p0, p1 in moves:
        cols[p1] = cols[p0][:n][::step] + cols[p1]
        cols[p0] = cols[p0][n:]
    result = "".join([v0 for v0, *_ in cols.values()])
    print(f"part {part}:", result)
