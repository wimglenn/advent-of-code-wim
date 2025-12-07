"""
--- Day 7: Laboratories ---
https://adventofcode.com/2025/day/7
"""

from aocd import data

lines = data.splitlines()
w = len(lines[0])
beams = [0] * w
beams[lines[0].index("S")] += 1
splitters = [{i for i, x in enumerate(line) if x == "^"} for line in lines[2::2]]

a = 0
for xs in splitters:
    new_beams = [0] * w
    for i, count in enumerate(beams):
        if count:
            if i in xs:
                a += 1
                new_beams[i - 1] += count
                new_beams[i + 1] += count
            else:
                new_beams[i] += count
    beams = new_beams
b = sum(beams)
print("answer_a:", a)
print("answer_b:", b)
