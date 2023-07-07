"""
--- Day 20: Grove Positioning System ---
https://adventofcode.com/2022/day/20
"""
from aocd import data


for key, rounds, part in zip((1, 811589153), (1, 10), "ab"):
    ns = [int(n) * key for n in data.split()]
    N = len(ns)
    idx = [*range(N)]
    for _ in range(rounds):
        for i in range(N):
            idx.pop(pos := idx.index(i))
            idx.insert((pos + ns[i]) % (N - 1), i)
    i0 = idx.index(ns.index(0))  # where did 0 get 'mixed' to?
    result = sum(ns[idx[(i0 + i) % N]] for i in [1000, 2000, 3000])
    print(f"answer_{part}:", result)
