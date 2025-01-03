"""
--- Day 16: Dragon Checksum ---
https://adventofcode.com/2016/day/16
"""
from aocd import data
from aocd import extra


def dragon(a):
    return a + "0" + "".join([{"0": "1", "1": "0"}[x] for x in a[::-1]])


def pad(s, n):
    return pad(dragon(s), n) if len(s) < n else s[:n]


def checksum(s):
    return "".join(["01"[a == b] for a, b in zip(s[0::2], s[1::2])])


def r_checksum(s):
    s = checksum(s)
    return s if len(s) % 2 else r_checksum(s)


def f(data, length):
    return r_checksum(pad(data, length))


if __name__ == "__main__":
    disk_length = extra.get("disk_length", 272)
    print("answer_a:", f(data, disk_length))
    if not extra:
        print("answer_b:", f(data, 35651584))
