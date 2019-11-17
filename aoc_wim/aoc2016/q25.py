import re

from aocd import data


def part_a(data):
    x, y = re.findall(r"\d+", data)[:2]
    return 0b101010101010 - int(x) * int(y)


print("part a:", part_a(data))
