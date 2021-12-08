"""
--- Day 14: Docking Data ---
https://adventofcode.com/2020/day/14
"""
from aocd import data
from itertools import combinations

da = {}
db = {}
for line in data.splitlines():
    if line.startswith("mask"):
        mask = line.split()[-1]
        on = int(mask.replace("X", "0"), 2)
        off = int(mask.replace("X", "1"), 2)
        Xi = [1 << i for i, v in enumerate(reversed(mask)) if v == "X"]
        nX = mask.count("X")
    else:
        mem, val = line.split(" = ")
        mem = int(mem.strip("mem[]"))
        val = int(val)
        da[mem] = (val | on) & off
        if nX > 10:
            # hackish: skip an extremely slow part b for the test of part a
            continue
        for r in range(nX + 1):
            for comb in combinations(Xi, r):
                memb = mem | on
                for bit in comb:
                    memb ^= bit
                db[memb] = val

print("part a:", sum(da.values()))
print("part b:", sum(db.values()))
