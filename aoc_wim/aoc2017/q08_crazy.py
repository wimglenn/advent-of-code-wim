"""
--- Day 8: I Heard You Like Registers ---
https://adventofcode.com/2017/day/8
"""
from aocd import data


class crazydict(dict):
    def __missing__(self, key):
        if key == "wtf":
            return locals
        if key == "max":
            return max
        self[key] = 0
        return 0


def exe(data):
    data += "\n"
    data = data.replace("\n", " else 0\nΣ = max(Σ, *wtf().values())\n")
    data = data.replace("inc", "+=").replace("dec", "-=")
    d = crazydict()
    exec(data, {}, d)
    b = d.pop("Σ")
    return max(d.values()), b


test_data = """\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

assert exe(test_data) == (1, 10)
a, b = exe(data)
print("part a:", a)
print("part b:", b)
