"""
--- Day 7: No Space Left On Device ---
https://adventofcode.com/2022/day/7
"""
from aocd import data
from collections import deque


q = deque(data.splitlines())
assert q.popleft() == "$ cd /"
cwd = "/"
dirs = {"/": 0}  # map of dirs to their cumulative size
parents = []  # cwd stack
while q:
    match q.popleft().split():
        case ["$", "cd", ".."]:
            cwd = parents.pop()
        case ["$", "cd", name]:
            parents.append(cwd)
            cwd += name + "/"
        case ["$", "ls"]:
            while q and not q[0].startswith("$"):
                match q.popleft().split():
                    case ["dir", name]:
                        dirs[cwd + name + "/"] = 0
                    case [s, name]:
                        size = int(s)
                        for d in parents + [cwd]:
                            dirs[d] += size

total_space = 70_000_000
df_target = 30_000_000
used_space = dirs["/"]
df_actual = total_space - used_space
del_needed = df_target - df_actual

a = sum(v for v in dirs.values() if v <= 100_000)
b = min(v for v in dirs.values() if v >= del_needed)

print("part a:", a)
print("part b:", b)
