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


data += "\n"
data = data.replace("\n", " else 0\nΣ = max(Σ, *wtf().values())\n")
data = data.replace("inc", "+=").replace("dec", "-=")
d = crazydict()
exec(data, {}, d)
b = d.pop("Σ")
print("answer_a:", max(d.values()))
print("answer_b:", b)
