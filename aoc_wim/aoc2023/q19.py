"""
--- Day 19: Aplenty ---
https://adventofcode.com/2023/day/19
"""
from dataclasses import dataclass
from dataclasses import replace
from math import prod

from aocd import data


workflows_raw, parts_raw = data.split("\n\n")

workflows = {}
for line in workflows_raw.splitlines():
    pk, w = line.rstrip("}").split("{")
    wf = []
    *rules, else_dst = w.split(",")
    for rule in rules:
        rule, dst = rule.split(":")
        op = "<" if "<" in rule else ">"
        ax, val = rule.split(op)
        wf.append((ax, op, int(val), dst))
    wf.append(else_dst)
    workflows[pk] = wf

parts = []
for r in parts_raw.splitlines():
    # just can't bring myself to use eval/exec
    part = {}
    for x_n in r.strip("{}").split(","):
        x, n = x_n.split("=")
        part[x] = int(n)
    parts.append(part)

a = 0
for part in parts:
    node = "in"
    while node not in "AR":
        *rules, else_dst = workflows[node]
        for rule in rules:
            ax, op, val, dst = rule
            result = part[ax] < val if op == "<" else part[ax] > val
            if result:
                node = dst
                break
        else:
            node = else_dst
    if node == "A":
        a += sum(part.values())
print("answer_a:", a)


@dataclass
class Block:
    x0: int = 1
    m0: int = 1
    a0: int = 1
    s0: int = 1
    x1: int = 4001
    m1: int = 4001
    a1: int = 4001
    s1: int = 4001

    @property
    def volume(self):
        return prod([
            self.x1 - self.x0,
            self.m1 - self.m0,
            self.a1 - self.a0,
            self.s1 - self.s0,
        ])

    def split(self, ax, op, val):
        if op == ">":
            return self.split(ax, "<", val + 1)[::-1]
        block_true = replace(self, **{f"{ax}1": val})
        block_false = replace(self, **{f"{ax}0": val})
        return block_true, block_false


b = 0
stack = [(Block(), "in")]
while stack:
    x, node = stack.pop()
    if node == "A":
        b += x.volume
        continue
    if node == "R":
        continue
    *rules, else_dst = workflows[node]
    for ax, op, val, dst in rules:
        xt, x = x.split(ax, op, val)
        stack.append((xt, dst))
    stack.append((x, else_dst))
print("answer_b:", b)
