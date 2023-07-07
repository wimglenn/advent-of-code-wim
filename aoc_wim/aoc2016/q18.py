"""
--- Day 18: Like a Rogue ---
https://adventofcode.com/2016/day/18
"""
from aocd import data


def generate_rows(row):
    """rule90"""
    idx = range(len(row))
    while True:
        yield row
        row = "." + row + "."
        row = "".join(["^."[row[i] == row[i + 2]] for i in idx])


n_rows = 3 if len(data) == 5 else 10 if len(data) == 10 else 40
gen = generate_rows(data)
safe = sum(next(gen).count(".") for _ in range(n_rows))
print("answer_a:", safe)
safe += sum(next(gen).count(".") for _ in range(400000 - n_rows))
print("answer_b:", safe)
