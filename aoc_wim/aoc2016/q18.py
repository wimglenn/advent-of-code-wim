"""
--- Day 18: Like a Rogue ---
https://adventofcode.com/2016/day/18
"""
from aocd import data
from aocd import extra


def generate_rows(row):
    """rule90: https://en.wikipedia.org/wiki/Rule_90"""
    idx = range(len(row))
    while True:
        yield row
        row = "." + row + "."
        row = "".join(["^."[row[i] == row[i + 2]] for i in idx])


n_rows = extra.get("n_rows", 40)
gen = generate_rows(data)
safe = sum(next(gen).count(".") for _ in range(n_rows))
print("answer_a:", safe)
safe += sum(next(gen).count(".") for _ in range(400000 - n_rows))
print("answer_b:", safe)
