"""
--- Day 22: Monkey Market ---
https://adventofcode.com/2024/day/22
"""
from aocd import data
import numpy as np
import regex as re


ns = [int(x) for x in data.split()]


def f(n):
    n ^= n << 6
    n %= 0x1000000
    n ^= n >> 5
    n %= 0x1000000
    n ^= n << 11
    n %= 0x1000000
    return n


nn = [ns]
for i in range(2000):
    nn.append([f(n) for n in nn[-1]])
a = sum(nn[-1])
print("answer_a:", a)

N = np.array(nn)
N1 = N % 10
delta = N1[1:] - N1[:-1]
ss = [",".join([format(x, " 2d") for x in col]) for col in delta.T]
ks = set(re.findall(r"[ -]\d,[ -]\d,[ -]\d,[ -]\d", "\n".join(ss), overlapped=True))
best = 0
for i, k in enumerate(ks):
    print(f"{i}/{len(ks)}")
    score = 0
    for s, n1 in zip(ss, N1.T):
        pos3 = s.find(k)
        if pos3 == -1:
            continue
        pos = pos3 // 3
        score += n1[pos + 4]
    if score > best:
        print(f"new best ({score}): {k}")
        best = score

b = int(best)
print("answer_b:", b)
