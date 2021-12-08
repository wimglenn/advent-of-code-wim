"""
--- Day 7: Some Assembly Required ---
https://adventofcode.com/2015/day/7
"""
import operator
import re

from aocd import data
import numpy as np


# TODO: change to use topological sort

opmap = {
    "AND": operator.and_,
    "OR": operator.or_,
    "LSHIFT": operator.lshift,
    "RSHIFT": operator.rshift,
}


def compute(data):
    result = {}

    def getval(v):
        return result[v] if v in result else np.uint16(v)

    lines = [line.split(" -> ") for line in data.splitlines()]

    def process_line(line):
        left, right = line
        left = left.split()
        len_left = len(left)
        if len_left == 1:
            # store
            result[right] = getval(left[0])
        elif len_left == 2:
            # negation
            op, val = left
            if op != "NOT":
                raise Exception
            result[right] = ~getval(val)
        elif len_left == 3:
            a, op, b = left
            op = opmap[op]
            result[right] = op(getval(a), getval(b))

    while lines:
        line = lines.pop()
        try:
            process_line(line)
        except (KeyError, ValueError):
            lines = [line] + lines

    return result


if __name__ == "__main__":
    result = compute(data)
    result_a = result["a"]
    print("part a:", result_a)

    new_data = re.sub(r"\n([0-9]+) -> b\n", "\n{} -> b\n".format(result_a), data)
    print("part b:", compute(new_data)["a"])
