import re
from aocd import data

x, y = re.findall(r"\d+", data)[:2]
a = 0b101010101010 - int(x) * int(y)
print("part a:", a)
