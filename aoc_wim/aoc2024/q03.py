"""
--- Day 3: Mull It Over ---
https://adventofcode.com/2024/day/3
"""
import parse
from aocd import data


pat = "mul({:d},{:d})"
a = sum(x * y for x, y in parse.findall(pat, data))
print("answer_a:", a)

while "don't()" in data:
    data, tail = data.split("don't()", 1)
    if "do()" in tail:
        data += tail.split("do()", 1)[1]
b = sum(x * y for x, y in parse.findall(pat, data))
print("answer_b:", b)
