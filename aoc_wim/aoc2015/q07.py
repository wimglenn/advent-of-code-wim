"""
--- Day 7: Some Assembly Required ---
https://adventofcode.com/2015/day/7
"""
import re
from collections import deque

import numpy as np
from aocd import data


def compute(data):
    wire = {}

    def get(v):
        return wire[v] if v in wire else np.uint16(v)

    q = deque(data.splitlines())
    while q:
        line = q.pop()
        try:
            match line.split():
                case n, "->", w:
                    wire[w] = get(n)
                case "NOT", n, "->", w:
                    wire[w] = ~get(n)
                case x, op, y, "->", w:
                    f = getattr(np.uint16, f"__{op}__".lower())
                    wire[w] = f(get(x), get(y))
        except (KeyError, ValueError):
            q.appendleft(line)

    return wire["a"]


a = compute(data)
print("answer_a:", a)

new_data = re.sub(r"\n([0-9]+) -> b\n", f"\n{a} -> b\n", data)
print("answer_b:", compute(new_data))
