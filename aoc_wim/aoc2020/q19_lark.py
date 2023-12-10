"""
--- Day 19: Monster Messages ---
https://adventofcode.com/2020/day/19
"""
import lark
from aocd import data


def solve(rules, messages):
    rules = rules.translate(str.maketrans("0123456789", "abcdefghij"))
    parser = lark.Lark(rules, start="a")
    result = 0
    for message in messages.splitlines():
        try:
            parser.parse(message)
        except lark.LarkError:
            pass
        else:
            result += 1
    return result


rules, messages = data.split("\n\n")
print("answer_a:", solve(rules, messages))

rules = rules.replace("8: 42", "8: 42 | 42 8").replace("11: 42 31", "11: 42 31 | 42 11 31")
print("answer_b:", solve(rules, messages))
