from aocd import data
import re

def part_a(data):
    x, y = re.findall(r'\d+', data)[:2]
    return int('0101010101010', 2) - int(x)*int(y)


print(part_a(data))  # part a: 198
