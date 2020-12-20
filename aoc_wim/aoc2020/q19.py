"""
--- Day 19: Monster Messages ---
https://adventofcode.com/2020/day/19
"""
from aocd import data
import regex as re


data = data.replace('"', '')
rules_raw, messages = data.split("\n\n")
messages = messages.splitlines()
rules = dict(line.split(": ") for line in rules_raw.splitlines())
digits = set("0123456789")


def eliminate(rules, k0):
    v0 = rules.pop(k0)
    if "|" in v0:
        v0 = f"( {v0} )"
    for k, v in rules.items():
        rules[k] = " ".join([v0 if k == k0 else k for k in v.split()])


def simplify(rules):
    rules = rules.copy()
    while True:
        for k, v in rules.items():
            if not digits.intersection(v):
                break
        else:
            return rules
        eliminate(rules, k)
        if len(rules) == 1:
            break
    return rules


rules_a = simplify(rules)
rule0_a = re.compile("^" + rules_a["0"].replace(" ", "") + "$")
print("part a:", sum(rule0_a.match(m) is not None for m in messages))

if {"8", "11"} < rules.keys():
    rules["8"] += " | 42 8"
    rules["11"] += " | 42 11 31"
    rules = simplify(rules)
    r0 = rules.pop("0")
    r8 = rules.pop("8")
    r11 = rules.pop("11")
    r8 = r8.replace(" ", "")
    r8 = r8[:-1]
    r8 = r8[:len(r8)//2]
    r8 = r8.replace("(", "(?:")
    r8 = "(" + r8 + ")+"
    r11 = r11.replace(" ", "")
    pre, post = r11.split("11")
    pre = pre[:pre.index(post)]
    pre = pre.replace("(", "(?:")
    post = post.replace("(", "(?:")
    r11 = "(" + pre + "(?2)?" + post + ")"
    rule0_b = re.compile("^" + r8 + r11 + "$")
    print("part b:", sum(rule0_b.match(m) is not None for m in messages))
