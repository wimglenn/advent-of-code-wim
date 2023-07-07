"""
--- Day 25: Full of Hot Air ---
https://adventofcode.com/2022/day/25
"""
from aocd import data


def snafu2dec(s):
    result = 0
    for i, char in enumerate(reversed(s)):
        n = -1 if char == "-" else -2 if char == "=" else int(char)
        result += n * (5 ** i)
    return result


def dec2snafu(n):
    result = []
    while n:
        n, r = divmod(n, 5)
        result.append(r)
    for i, val in enumerate(result):
        if val > 2:
            result[i] = "=" if val == 3 else "-" if val == 4 else 0
            try:
                result[i + 1] += 1
            except IndexError:
                result.append(1)
    return "".join(map(str, reversed(result)))


print("answer_a:", dec2snafu(sum(snafu2dec(n) for n in data.split())))
