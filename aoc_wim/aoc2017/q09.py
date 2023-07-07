"""
--- Day 9: Stream Processing ---
https://adventofcode.com/2017/day/9
"""
import re

from aocd import data


n_removed = 0
while "!!" in data:
    data = data.replace("!!", "")
data = re.sub("!.", "", data)
n_removed += len(data) - len(re.sub("<.*?>", "", data))
n_removed -= 2 * len(re.findall("<.*?>", data))
data = re.sub("<.*?>", "", data)
score = 0
nesting = 0
for c in data:
    if c == "{":
        nesting += 1
    elif c == "}":
        score += nesting
        nesting -= 1

print("answer_a:", score)
print("answer_b:", n_removed)
