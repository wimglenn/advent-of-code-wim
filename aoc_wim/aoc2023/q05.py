"""
--- Day 5: If You Give A Seed A Fertilizer ---
https://adventofcode.com/2023/day/5
"""
from aocd import data


chunks = data.split("\n\n")
seeds, *chunks = chunks
seeds = [int(x) for x in seeds.removeprefix("seeds:").split()]
mm = []
for chunk in chunks:
    _, *ranges = chunk.splitlines()
    m = []
    for r in ranges:
        dest, source, length = map(int, r.split())
        delta = dest - source
        m.append([source, source + length, delta])
    m.sort()
    m_new = []
    # fill any gaps
    for m1, m2 in zip(m, m[1:]):
        m_new.append(m1)
        if m1[1] < m2[0]:
            m_new.append([m1[1], m2[0], 0])
    m_new.extend(m[-1:])
    m[:] = m_new
    mm.append(m)

s_prev = seeds[:]
for m in mm:
    s_new = []
    for s in s_prev:
        for left, right, delta in m:
            if left <= s < right:
                s_new.append(s + delta)
                break
        else:
            s_new.append(s)
    s_prev[:] = s_new

a = min(s_prev)
print("answer_a:", a)

r_prev = [(s0, s0 + s1) for s0, s1 in zip(seeds[0::2], seeds[1::2])]
for m in mm:
    cuts = [left for left, right, delta in m]
    cuts.append(m[-1][1])
    r_new = []
    r_cut = []
    for L, R in r_prev:
        inside = [L] + [c for c in cuts if L < c < R] + [R]
        r_cut.extend(zip(inside, inside[1:]))
    for left0, right0 in r_cut:
        for left, right, d in m:
            if left <= left0 < right0 <= right:
                break
        else:
            d = 0
        r_new.append((left0 + d, right0 + d))
    r_prev[:] = r_new

b = min(left for left, right in r_prev)
print("answer_b:", b)
