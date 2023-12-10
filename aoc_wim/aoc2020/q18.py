"""
--- Day 18: Operation Order ---
https://adventofcode.com/2020/day/18
"""
from collections import deque

from aocd import data


def evaluate(d, part="a"):
    op = "*"
    val = None
    prev = 1
    while d:
        tok = d.popleft()
        if tok == "(":
            val = evaluate(d, part=part)
        elif tok.isdigit():
            val = int(tok)
        elif tok in "+*":
            op = tok
        elif tok == ")":
            return prev
        if val is not None:
            if op == "+":
                prev += val
            elif op == "*":
                if part == "b":
                    while d and d[0] == "+":
                        d.popleft()
                        r = d.popleft()
                        if r.isdigit():
                            val += int(r)
                        elif r == "(":
                            val += evaluate(d, part=part)
                prev *= val
            val = None
    return prev


lines = data.replace(" ", "").splitlines()
print("answer_a:", sum([evaluate(deque(line), part="a") for line in lines]))
print("answer_b:", sum([evaluate(deque(line), part="b") for line in lines]))
