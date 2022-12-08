"""
--- Day 7: No Space Left On Device ---
https://adventofcode.com/2022/day/7
"""
from aocd import data
from pathlib import Path
from collections import Counter

cwd = Path()
dirs = Counter()

for line in data.splitlines():
    match line.split():
        case ["$", "cd", name]: cwd = cwd.joinpath(name).resolve()
        case [s, name] if s.isdigit():
            for p in [cwd, *cwd.parents]:
                dirs[p] += int(s)

rmbytes = dirs[Path("/")] - 70_000_000 + 30_000_000
a = sum(v for v in dirs.values() if v <= 100_000)
b = min(v for v in dirs.values() if v >= rmbytes)

print("part a:", a)
print("part b:", b)
