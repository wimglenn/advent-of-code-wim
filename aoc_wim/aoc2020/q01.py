from collections import Counter
from aocd import data

counter = Counter(int(x) for x in data.splitlines())


def find_pair(counter, target=2020):
    # find a pair of numbers from the multiset (counter) which sums to target
    for number in counter:
        diff = target - number
        if diff in counter:
            if diff == number and counter[number] <= 1:
                continue
            return number, diff


x, y = find_pair(counter)
print(f"part a: {x} * {y} == {x * y}")

for z in list(counter):
    counter[z] -= 1
    pair = find_pair(counter, target=2020 - z)
    if pair:
        x, y = pair
        print(f"part b: {x} * {y} * {z} == {x * y * z}")
        break
