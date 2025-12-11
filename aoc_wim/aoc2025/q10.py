"""
--- Day 10: Factory ---
https://adventofcode.com/2025/day/10
"""

from collections import deque
from aocd import data
from scipy.optimize import linprog

tr = str.maketrans("#.", "10", "()[]{}")
data = data.translate(tr)
lights = []
buttons_a = []
buttons_b = []
jolts = []
for line in data.splitlines():
    light, *buttons, jolt = line.split()
    n = len(light)
    buttons = [(*map(int, x.split(",")),) for x in buttons]
    lights.append(int(light[::-1], 2))
    buttons_a.append([sum(1 << x for x in b) for b in buttons])
    buttons_b.append([[int(i in b) for b in buttons] for i in range(n)])
    jolts.append([int(x) for x in jolt.split(",")])

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

b = 0
for buttons, jolt in zip(buttons_b, jolts):
    c = [1] * len(buttons[0])
    prog = linprog(c, A_eq=buttons, b_eq=jolt, integrality=1)
    b += round(prog.fun)
print("answer_b:", b)
