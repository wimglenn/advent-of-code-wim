"""
--- Day 10: Factory ---
https://adventofcode.com/2025/day/10
"""

from collections import deque
from aocd import data
from aoc_wim.stuff import change_making

# data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
# [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
# """

tr = str.maketrans("#.", "10", "()[]{}")
data = data.translate(tr)

lights = []
buttons_a = []
buttons_b = []
jolts = []
for line in data.splitlines():
    light, *buttons, jolt = line.split()
    n = len(light)
    lights.append(int(light[::-1], 2))
    jolts.append([int(x) for x in jolt.split(",")])
    ba = []
    bb = []
    for button in buttons:
        ns = [int(x) for x in button.split(",")]
        ba.append(sum(1 << x for x in ns))
        bb.append([1 if i in ns else 0 for i in range(n)])
    bb.sort(key=sum, reverse=True)
    buttons_a.append(ba)
    buttons_b.append(bb)

a = 0
for light, button in zip(lights, buttons_a):
    q = deque([(0, 0)])
    seen = set()
    while q:
        n, count = q.popleft()
        if n == light:
            a += count
            break
        if n not in seen:
            q += [(n ^ b, count + 1) for b in button]
            seen.add(n)
print("answer_a:", a)

scalar_buttons = []
scalar_jolts = []
for buttons, jolt in zip(buttons_b, jolts):
    # pack buttons and target joltage vectors into scalars for speed.
    # find the smallest power of 2 which is bigger than max jolts and rebase.
    max_jolt = max(jolt)
    f = 1
    while 2 ** f < max_jolt:
        f += 1
    s_buttons = [sum(x * (1 << i * f) for i, x in enumerate(b)) for b in buttons]
    s_buttons.sort(reverse=True)
    scalar_buttons.append(s_buttons)
    scalar_jolts.append(sum(x * (1 << i * f) for i, x in enumerate(jolt)))

b = 0
for buttons, jolt in zip(scalar_buttons, scalar_jolts):
    count = change_making(coins=buttons, n=jolt)
    b += count
    print("--->", jolt, count, b)

    # q = deque([(jolt, 0)])
    # seen = set()
    # while q:
    #     j0, count = q.popleft()
    #     if not j0:
    #         b += count
    #         print("--->", jolt, count, b)
    #         break
    #     if j0 not in seen:
    #         q += [(j0 - b, count + 1) for b in buttons if j0 - b >= 0]
    #         seen.add(j0)

print("answer_b:", b)
