"""
--- Day 11: Dumbo Octopus ---
https://adventofcode.com/2021/day/11
"""
from aocd import data
from aoc_wim.zgrid import ZGrid


g = ZGrid(data, transform=int)
a = b = 0
while True:
    b += 1
    n = 0
    flash = []
    for z in g:
        if g[z] == 9:
            g[z] = 0
            flash.append(z)
        else:
            g[z] += 1
    while flash:
        z0 = flash.pop()
        n += 1
        for z in g.near(z0, n=8):
            if g.get(z):
                if g[z] == 9:
                    g[z] = 0
                    flash.append(z)
                else:
                    g[z] += 1
    if b <= 100:
        a += n
    if n == len(g):
        break

print("part a:", a)
print("part b:", b)
