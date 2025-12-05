"""
--- Day 5: Cafeteria ---
https://adventofcode.com/2025/day/5
"""

from aocd import data

rs, ns = data.split("\n\n")
ns = [int(x) for x in ns.split()]
rs = sorted([[*map(int, x.split("-"))] for x in rs.split()])
merged = [rs[0]]
for r in rs:
    if r[0] > merged[-1][1]:
        merged.append(r)
    else:
        merged[-1][1] = max(merged[-1][1], r[1])

print("answer_a:", sum(any(x <= n <= y for x, y in merged) for n in ns))
print("answer_b:", sum(y - x + 1 for x, y in merged))
