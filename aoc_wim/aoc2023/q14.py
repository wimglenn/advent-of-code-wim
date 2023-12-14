"""
--- Day 14: Parabolic Reflector Dish ---
https://adventofcode.com/2023/day/14
"""
from aocd import data


def tilt_north(data):
    rows = data.splitlines()
    cols = [''.join(col) for col in list(zip(*rows))]
    newcols = []
    for col in cols:
        segments = col.split("#")
        segments = [''.join(sorted(s, reverse=True)) for s in segments]
        newcol = "#".join(segments)
        newcols.append(newcol)
    newrows = [''.join(row) for row in list(zip(*newcols))]
    newdata = "\n".join(newrows)
    return newdata


def rotate_right(data):
    rows = data.splitlines()
    cols = [''.join(col) for col in list(zip(*rows))]
    return "\n".join([col[::-1] for col in cols])


def one_cycle(data):
    for _ in "NWSE":
        data = tilt_north(data)
        data = rotate_right(data)
    return data


def load_on_north_support_beams(rows):
    return sum(i*row.count("O") for i, row in enumerate(rows.splitlines()[::-1], 1))


print("answer_a:", load_on_north_support_beams(tilt_north(data)))
cycles = 1_000_000_000
seen = {}
period = None
i = 0
while i < cycles:
    data = one_cycle(data)
    i += 1
    # print(f"After {i+1} cycle:\n{data}\n\n")
    if period is None and data in seen:
        period = i - seen[data]
        i += period * ((cycles - i) // period)
    seen[data] = i
print("answer_b:", load_on_north_support_beams(data))
