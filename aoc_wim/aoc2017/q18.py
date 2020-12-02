"""
--- Day 18: Duet ---
https://adventofcode.com/2017/day/18
"""
from collections import deque

from aocd import data


# TODO: change to OOP comp

def run_a(data):
    snd = None
    lines = data.splitlines()
    d = {line[4:5]: 0 for line in lines if not line[4:5].isdigit()}
    i = 0
    while True:
        line = lines[i]
        if line.startswith("snd"):
            _snd, k = line.split()
            try:
                snd = d[k]
            except KeyError:
                return
        elif line.startswith("rcv"):
            _rcv, k = line.split()
            if d[k]:
                return snd
        else:
            op, k, n = line.split()
            n = d[n] if n in d else int(n)
            if op == "set":
                d[k] = n
            elif op == "add":
                d[k] += n
            elif op == "mul":
                d[k] *= n
            elif op == "mod":
                d[k] %= n
            elif op == "jgz":
                k = d[k] if k in d else int(k)
                i += n - 1 if k > 0 else 0
        i += 1


def run_b(data, p, q):
    lines = data.splitlines()
    d = {line[4:5]: 0 for line in lines if not line[4:5].isdigit()}
    d["p"] = p
    i = 0
    while True:
        line = lines[i]
        if line.startswith("snd"):
            _snd, n = line.split()
            n = d[n] if n in d else int(n)
            yield n
        elif line.startswith("rcv"):
            _rcv, k = line.split()
            try:
                d[k] = q.popleft()
            except IndexError:
                i -= 1
                yield
        else:
            op, k, n = line.split()
            n = d[n] if n in d else int(n)
            if op == "set":
                d[k] = n
            elif op == "add":
                d[k] += n
            elif op == "mul":
                d[k] *= n
            elif op == "mod":
                d[k] %= n
            elif op == "jgz":
                k = d[k] if k in d else int(k)
                i += n - 1 if k > 0 else 0
        i += 1


def part_b(data):
    q0 = deque()
    q1 = deque()
    g0 = run_b(data, p=0, q=q0)
    g1 = run_b(data, p=1, q=q1)
    p1_sent = 0
    while True:
        n0, n1 = next(g0), next(g1)
        if n0 is not None:
            q1.append(n0)
        if n1 is not None:
            q0.append(n1)
            p1_sent += 1
        if n0 is n1 is None:
            return p1_sent


print("part a:", run_a(data))
print("part b:", part_b(data))
