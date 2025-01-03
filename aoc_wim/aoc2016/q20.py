"""
--- Day 20: Firewall Rules ---
https://adventofcode.com/2016/day/20
"""
from aocd import data
from aocd import extra


ns = [*map(int, data.replace("-", " ").split())]
intervals = sorted(zip(ns[0::2], ns[1::2]))
while True:
    n = len(intervals)
    for i in range(n - 1):
        lo_p, hi_p = intervals[i]
        lo, hi = intervals[i + 1]
        if lo <= hi_p + 1:
            del intervals[i + 1]
            intervals[i] = lo_p, max(hi_p, hi)
            break
    else:
        break

print("answer_a:", intervals[0][1] + 1)

b = extra.get("max_val", 4294967295) + 1
for lo, high in intervals:
    b -= high - lo + 1
print("answer_b:", b)
