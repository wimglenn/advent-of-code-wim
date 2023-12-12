"""
--- Day 12: Hot Springs ---
https://adventofcode.com/2023/day/12
"""
from aocd import data
from functools import cache


def fits(template, counts, n_free):
    if n_free == 0:
        actual = [len(s) for s in template.replace("?", ".").split(".") if s]
        return actual == counts
    if "?" not in template:
        return 0
    new1 = template.replace("?", ".", 1)
    new2 = template.replace("?", "#", 1)
    return fits(new1, counts, n_free) + fits(new2, counts, n_free - 1)


a = b = 0
for line in data.splitlines():
    template, counts = line.split()
    template_b = "?".join([template]*5)
    counts = [int(x) for x in counts.split(",")]
    counts_b = counts*5
    n_free = sum(counts) - template.count("#")
    n_free_b = n_free * 5 + 4
    da = fits(template, counts, n_free)
    a += da
    # print(line)
    # db = fits(template_b, counts_b, n_free_b)
    # b += db


print("answer_a:", a)
print("answer_b:", b)

# from aocd import submit; submit(a)
