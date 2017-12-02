from aocd import data
from itertools import combinations

test_a = '''5 1 9 5
7 5 3
2 4 6 8
'''

def checksum_a(data):
    result = 0
    for line in data.splitlines():
        row = [int(x) for x in line.split()]
        result += max(row) - min(row)
    return result

test_b = '''5 9 2 8
9 4 7 3
3 8 6 5'''

def checksum_b(data):
    result = 0
    for line in data.splitlines():
        row = [int(x) for x in line.split()]
        for x, y in combinations(row, 2):
            denominator, numerator = sorted([x, y])
            quotient, remainder = divmod(numerator, denominator)
            if not remainder:
                result += quotient
                continue
    return result

assert checksum_a(test_a) == 18
print(checksum_a(data))  # part a: 45972

assert checksum_b(test_b) == 9
print(checksum_b(data))  # part b: 326
