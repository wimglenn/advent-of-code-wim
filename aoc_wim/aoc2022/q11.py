"""
--- Day 11: Monkey in the Middle ---
https://adventofcode.com/2022/day/11
"""
from aocd import data
from parse import parse
from collections import deque
from heapq import nlargest
from math import prod


template = """\
Monkey {id:d}:
  Starting items: {items}
  Operation: new = {x1} {op} {x2}
  Test: divisible by {div:d}
    If true: throw to monkey {mt:d}
    If false: throw to monkey {mf:d}"""


class Monkey:

    def __init__(self, items, x1, op, x2, div, mt, mf):
        self.items = items
        self.x1 = x1
        self.op = op
        self.x2 = x2
        self.div = div
        self.mt = mt
        self.mf = mf
        self.inspected = 0

    @classmethod
    def fromchunk(cls, chunk):
        parsed = parse(template, chunk).named
        items = deque(map(int, parsed.pop("items").split(", ")))
        parsed.pop("id")
        return cls(items, **parsed)

    def inspect(self):
        while self.items:
            item = self.items.popleft()
            self.inspected += 1
            x1 = item if self.x1 == "old" else int(self.x1)
            x2 = item if self.x2 == "old" else int(self.x2)
            val = x1 + x2 if self.op == "+" else x1 * x2
            val = val // 3 if part == "a" else val % denom
            mnext = self.mf if val % self.div else self.mt
            monkeys[mnext].items.append(val)


for part, nrounds in zip("ab", (20, 10000)):
    monkeys = [Monkey.fromchunk(x) for x in data.split("\n\n")]
    denom = prod([m.div for m in monkeys])
    for round in range(nrounds):
        for monkey in monkeys:
            monkey.inspect()
    print(f"part {part}:", prod(nlargest(2, [m.inspected for m in monkeys])))
