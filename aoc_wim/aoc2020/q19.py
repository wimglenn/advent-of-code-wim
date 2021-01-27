"""
--- Day 19: Monster Messages ---
https://adventofcode.com/2020/day/19
"""
from aocd import data
import regex as re


rules_raw, messages = data.replace('"', "").split("\n\n")
messages = messages.splitlines()
rules = dict(line.split(": ") for line in rules_raw.splitlines())
digits = set("0123456789")


def eliminate(rules, k0):
    v0 = rules.pop(k0)
    if "|" in v0:
        v0 = f"( {v0} )"
    for k, v in rules.items():
        rules[k] = " ".join([v0 if k == k0 else k for k in v.split()])
    return v0.replace(" ", "")


def simplify(rules):
    solved = {}
    unsolved = rules.copy()
    while True:
        for k, v in unsolved.items():
            if not digits.intersection(v):
                break
        else:
            break
        solved[k] = eliminate(unsolved, k)
    return solved, unsolved


solved, unsolved = simplify(rules)
r0a = re.compile("^" + solved["0"].replace(" ", "") + "$")
print("part a:", sum(r0a.match(m) is not None for m in messages))

if {"8", "11"} < rules.keys():
    rules["8"] += " | 42 8"
    rules["11"] += " | 42 11 31"
    solved, unsolved = simplify(rules)
    r42 = solved["42"].replace("(", "(?:")  # non-capture
    r31 = solved["31"].replace("(", "(?:")  # non-capture
    r8 = "(" + r42 + ")+"
    r11 = "(" + r42 + "(?2)?" + r31 + ")"
    r0b = re.compile("^" + r8 + r11 + "$")
    print("part b:", sum(r0b.match(m) is not None for m in messages))
