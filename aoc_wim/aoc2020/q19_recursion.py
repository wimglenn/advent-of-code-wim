"""
--- Day 19: Monster Messages ---
https://adventofcode.com/2020/day/19
"""
from aocd import data


def match(message, remaining):
    if not message or not remaining:
        return not message and not remaining
    first, *rest = remaining
    rule = rules[first]
    if rule in ("a", "b"):
        if message.startswith(rule):
            return match(message[1:], rest)
        return False
    return any(match(message, t + rest) for t in rule)


rules_raw, messages = data.replace('"', "").split("\n\n")
messages = messages.splitlines()
rules = dict(r.split(": ") for r in rules_raw.splitlines())
for k, v in rules.items():
    if v not in "ab":
        rules[k] = [t.split() for t in v.split("|")]

print("part a:", sum(match(m, ["0"]) for m in messages))

rules["8"].append(["42", "8"])
rules["11"].append(["42", "11", "31"])
print("part b:", sum(match(m, ["0"]) for m in messages))
