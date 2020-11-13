"""
--- Day 7: Internet Protocol Version 7 ---
https://adventofcode.com/2016/day/7
"""
import re

from aocd import data


def splitter(s):
    pattern = r"\[([a-z]*)\]"
    ins = re.findall(pattern, s)
    outs = re.sub(pattern, " ", s).split()
    return ins, outs


def chunker(s, size):
    i = 0
    while True:
        chunk = s[i : i + size]
        if len(chunk) != size:
            break
        yield chunk
        i += 1


def has_abba(s):
    for a, b, b_, a_ in chunker(s, 4):
        if a == a_ and b == b_ and a != b:
            return True
    return False


def gen_aba(s):
    for a, b, a_ in chunker(s, 3):
        if a == a_ and a != b:
            yield a + b + a


def has_aba(s):
    return bool(next(gen_aba(s), False))


def support_tls(s):
    ins, outs = splitter(s)
    return has_abba(".".join(outs)) and not has_abba(".".join(ins))


def support_ssl(s):
    ins, outs = splitter(s)
    for a, b, a in gen_aba("..".join(ins)):
        bab = b + a + b
        if bab in "..".join(outs):
            return True
    return False


tls = ssl = 0
for line in data.splitlines():
    tls += support_tls(line)
    ssl += support_ssl(line)

print(tls)
print(ssl)
