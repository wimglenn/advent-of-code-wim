"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---
https://adventofcode.com/2015/day/5
"""
from aocd import data


def vowel_count(s):
    vowels = set("aeiou")
    return sum(1 for c in s if c in vowels)


def has_double(s):
    for left, right in zip(s[:-1], s[1:]):
        if left == right:
            return True


def blacklisted(s):
    for substring in "ab", "cd", "pq", "xy":
        if substring in s:
            return True


def has_pair(s):
    for left, right in zip(s[:-1], s[1:]):
        if s.count(left + right) > 1:
            return True


def has_skip_repeat(s):
    for left, right in zip(s[:-2], s[2:]):
        if left == right:
            return True


def is_nice_a(s):
    return vowel_count(s) >= 3 and has_double(s) and not blacklisted(s)


def is_nice_b(s):
    return has_pair(s) and has_skip_repeat(s)


words = data.splitlines()
print("part a:", len([w for w in words if is_nice_a(w)]))
print("part b:", len([w for w in words if is_nice_b(w)]))
