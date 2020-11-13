"""
--- Day 22: Slam Shuffle ---
https://adventofcode.com/2019/day/22
"""
from math import prod
from aocd import data


def parsed(data):
    # decompose "flip" operations into cut + stride
    data = data.replace("deal into new stack", "cut -1\ndeal with increment -1")
    ops = []
    for line in data.splitlines():
        op, *crap, n = line.split()
        n = int(n)
        assert op in {"cut", "deal"}
        ops.append((op, n))
    return ops


def simplify(ops, N, repeats=1):
    done = False
    while not done:
        done = True
        for i in range(1, len(ops)):
            op_prev, n_prev = ops[i - 1]
            op, n = ops[i]
            if op == "cut" and op_prev == "deal":
                # bubble all the cuts up to the top
                n_cut = (n * pow(n_prev, N - 2, N)) % N
                ops[i] = op_prev, n_prev
                ops[i - 1] = op, n_cut
                done = False
    # merge all the rotations
    n_cut = sum(n for op, n in ops if op == "cut") % N
    # merge all the strides
    n_deal = prod(n for op, n in ops if op == "deal") % N
    ops[:] = [("cut", n_cut), ("deal", n_deal)]
    if repeats > 1:
        compress(ops, N, repeats)


def compress(ops, N, repeats):
    assert len(ops) == 2
    result = []
    while repeats > 1:
        if repeats % 2:
            result = ops + result
            repeats -= 1
        repeats //= 2
        ops *= 2
        simplify(ops, N)
    result = ops + result
    simplify(result, N)
    ops[:] = result


def part_a(data, N=10007, pos=2019):
    ops = parsed(data)
    simplify(ops, N)
    [(cut, c0), (deal, f)] = ops
    result = f * (pos - c0) % N
    return result


def part_b(data, N=119315717514047, n_shuffles=101741582076661, card=2020):
    ops = parsed(data)
    simplify(ops, N, n_shuffles)
    [(cut, c0), (deal, f)] = ops
    # fermat's little theorem - modular multiplicative inverse
    # trick works because N is prime (!)
    result = (c0 + card * pow(f, N - 2, N)) % N
    return result


print("part a", part_a(data))
print("part b", part_b(data))
