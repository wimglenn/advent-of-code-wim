"""
--- Day 11: Plutonian Pebbles ---
https://adventofcode.com/2024/day/11
"""
from aocd import data
from collections import Counter


def blink(d):
    result = Counter()
    for k, n in d.items():
        if k == "0":
            result["1"] += n
        elif len(k) % 2 == 0:
            i = len(k) // 2
            result[k[:i].lstrip("0") or "0"] += n
            result[k[i:].lstrip("0") or "0"] += n
        else:
            result[str(int(k) * 2024)] += n
    return result


stones = Counter(data.split())
for i in range(25):
    stones = blink(stones)
print("answer_a:", sum(stones.values()))

for i in range(50):
    stones = blink(stones)
print("answer_b:", sum(stones.values()))
