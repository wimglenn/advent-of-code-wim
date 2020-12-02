"""
--- Day 1: Report Repair ---
https://adventofcode.com/2020/day/1
"""
from collections import Counter
from aocd import data


def find_pair(counter, target=2020):
    # find a pair of numbers from the multiset (counter) which sums to target
    for number in counter:
        diff = target - number
        if diff in counter:
            if diff == number and counter[number] <= 1:
                continue
            return number, diff


counter = Counter(int(x) for x in data.splitlines())
x, y = find_pair(counter)
print(f"part a: {x} * {y} == {x * y}")

for z in list(counter):
    counter[z] -= 1
    try:
        x, y = find_pair(counter, target=2020 - z)
    except TypeError:
        counter[z] += 1
    else:
        print(f"part b: {x} * {y} * {z} == {x * y * z}")
        break
