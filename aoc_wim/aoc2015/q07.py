import operator
import re

from aocd import data
from numpy import uint16


opmap = {
    "AND": operator.and_,
    "OR": operator.or_,
    "LSHIFT": operator.lshift,
    "RSHIFT": operator.rshift,
}


def compute(data):
    result = {}

    def getval(v):
        return result[v] if v in result else uint16(v)

    lines = data.splitlines()
    lines = [line.partition(" -> ")[::2] for line in lines]

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


test_data = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

test_result = {
    "d": 72,
    "e": 507,
    "f": 492,
    "g": 114,
    "h": 65412,
    "i": 65079,
    "x": 123,
    "y": 456,
}

assert compute(test_data) == test_result

result = compute(data)
result_a = result["a"]
print("part a:", result_a)

new_data = re.sub(r"\n([0-9]+) -> b\n", "\n{} -> b\n".format(result_a), data)
print("part b:", compute(new_data)["a"])
