"""
--- Day 15: Lens Library ---
https://adventofcode.com/2023/day/15
"""
from aocd import data


def keyfunc(s):
    i = 0
    for char in s:
        i += ord(char)
        i *= 17
        i %= 256
    return i


hashmap = [{} for i in range(256)]
for op in data.split(","):
    match op.strip("-").split("="):
        case [k, v]: hashmap[keyfunc(k)][k] = int(v)
        case [k]: hashmap[keyfunc(k)].pop(k, None)

print("answer_a:", sum(keyfunc(op) for op in data.split(",")))
print("answer_b:", sum(i*sum(k*v for k,v in enumerate(box.values(),1)) for i,box in enumerate(hashmap,1)))
