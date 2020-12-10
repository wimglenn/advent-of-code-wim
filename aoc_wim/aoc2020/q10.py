"""
--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10
"""
from aocd import data

numbers = [int(x) for x in data.split()]
numbers.append(0)  # outlet
numbers.sort()
numbers.append(numbers[-1] + 3)  # device
s0 = s = "".join([str(y - x) for x, y in zip(numbers, numbers[1:])])
print("part a:", s.count("1") * s.count("3"))
d = {
    "1111": 7,
    "111": 4,
    "11": 2,
}
b = 1
for k, v in d.items():
    b *= v ** s.count(k)
    s = s.replace(k, "")
print("part b:", b)
