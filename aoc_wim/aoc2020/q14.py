"""
--- Day 14: Docking Data ---
https://adventofcode.com/2020/day/14
"""
from aocd import data

da = {}
db = {}
for line in data.splitlines():
    if line.startswith("mask"):
        mask = line.split()[-1]
        ones = int(mask.replace("X", "0"), 2)
        zeros = int(mask.replace("X", "1"), 2)
        Xi = [2 ** (35 - i) for i, v in enumerate(mask) if v == "X"]
        nX = mask.count("X")
    else:
        mem, _, val = line.partition(" = ")
        mem = int(mem.strip("mem[]"))
        val = int(val)
        da[mem] = (val | ones) & zeros
        if nX > 10:
            # hackish: skip an extremely slow part b for the test of part a
            continue
        for i in range(2 ** nX):
            s = f"{i:0{nX}b}"
            onesb = sum(Xi[j] for j, char in enumerate(s) if char == "1")
            zerosb = 2**36 - 1 - sum(Xi[j] for j, char in enumerate(s) if char == "0")
            memb = (mem | ones | onesb) & zerosb
            db[memb] = val

print("part a:", sum(da.values()))
print("part b:", sum(db.values()))
