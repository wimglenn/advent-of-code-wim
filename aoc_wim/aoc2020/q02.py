"""
--- Day 2: Password Philosophy ---
https://adventofcode.com/2020/day/2
"""
from aocd import data
from parse import parse

a = b = 0
for line in data.splitlines():
    x, y, char, passwd = parse("{:d}-{:d} {}: {}", line)
    a += x <= passwd.count(char) <= y
    b += (passwd[x - 1] + passwd[y - 1]).count(char) == 1

print(a)
print(b)
