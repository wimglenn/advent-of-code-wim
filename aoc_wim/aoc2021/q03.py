"""
--- Day 3: Binary Diagnostic ---
https://adventofcode.com/2021/day/3
"""
from aocd import data


rows = data.splitlines()
cols = ["".join(c) for c in zip(*rows)]
h2 = len(rows) // 2
n = "".join("10"[c.count("1") >= h2] for c in cols)
𝛾 = int(n, 2)
ε = 𝛾 ^ 2 ** len(n) - 1
print("part a:", 𝛾 * ε)

life_support = 1
s = "01"
for _ in s:
    i = 0
    ns = rows.copy()
    while len(ns) > 1:
        col = [n[i] for n in ns]
        b = col.count("1") >= col.count("0")
        ns = [n for n in ns if n[i] == s[b]]
        i += 1
    [n] = ns
    life_support *= int(n, 2)
    s = s[::-1]
print("part b:", life_support)
