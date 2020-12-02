"""
--- Day 16: Permutation Promenade ---
https://adventofcode.com/2017/day/16
"""
from aocd import data


def parsed(data, mod=16):
    S = 0
    ops = []
    for op in data.split(","):
        if op.startswith("s"):
            n = int(op[1:])
            S += n
        elif op.startswith("x"):
            a, b = op[1:].split("/")
            a = (int(a) - S) % mod
            b = (int(b) - S) % mod
            ops.append(("x", a, b))
        elif op.startswith("p"):
            a, b = op[1:].split("/")
            ops.append(("p", a, b))
    ops.append(("s", S % mod, S % mod))
    return ops


def dance(data, d, n=1):
    mod = len(d)
    ops = parsed(data, mod=mod)
    seen = {}
    while n:
        s = "".join(d)
        if s in seen:
            r = seen[s] - n
            n %= r
            seen.clear()
            continue
        seen[s] = n
        for i, a, b in ops:
            if i == "x":
                d[a], d[b] = d[b], d[a]
            elif i == "p":
                ai = d.index(a)
                bi = d.index(b)
                d[ai], d[bi] = d[bi], d[ai]
            elif i == "s":
                d[:] = d[(mod - a) :] + d[: (mod - a)]
        n -= 1
    return "".join(d)


d = list("abcdefghijklmnop")
print("part a:", dance(data, d))
print("part b:", dance(data, d, n=1000000000 - 1))
