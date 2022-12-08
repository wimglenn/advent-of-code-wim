"""
--- Day 7: No Space Left On Device ---
https://adventofcode.com/2022/day/7
"""
from aocd import data
from pathlib import Path

cwd = Path()
dirs = {}

for line in data.splitlines():
    match line.split():
        case ["$", "cd", "/"]:
            cwd = Path("/")
            dirs[cwd] = 0
        case ["$", "cd", ".."]:
            cwd = cwd.parent
        case ["$", "cd", name]:
            cwd /= name
        case ["$", "ls"]:
            pass
        case ["dir", name]:
            dirs[cwd / name] = 0
        case [s, name]:
            size = int(s)
            for p in [cwd, *cwd.parents]:
                dirs[p] += size

total_space = 70_000_000
df_target = 30_000_000
used_space = dirs[Path("/")]
df_actual = total_space - used_space
del_needed = df_target - df_actual

a = sum(v for v in dirs.values() if v <= 100_000)
b = min(v for v in dirs.values() if v >= del_needed)

print("part a:", a)
print("part b:", b)
