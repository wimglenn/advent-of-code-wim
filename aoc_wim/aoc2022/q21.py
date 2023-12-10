"""
--- Day 21: Monkey Math ---
https://adventofcode.com/2022/day/21
"""
import operator as op

from aocd import data

ops = {
    "+": op.add,
    "*": op.mul,
    "-": op.sub,
    "/": op.truediv,
}


def solve(eqns):
    known = {}
    unknown = eqns.copy()
    while unknown:
        for name, eqn in unknown.items():
            if eqn in known or isinstance(eqn, complex) or eqn.isdigit():
                known[name] = complex(known.get(eqn, eqn))
                del unknown[name]
                break
            e1, o, e2 = eqn.split()
            if e1 in known or e1.isdigit():
                e1 = complex(known.get(e1, e1))
            if e2 in known or e2.isdigit():
                e2 = complex(known.get(e2, e2))
            if type(e1) is type(e2) is complex:
                known[name] = ops[o](e1, e2)
                del unknown[name]
                break
    return known


eqns = dict(line.split(": ") for line in data.splitlines())
known = solve(eqns)
print("answer_a:", int(known["root"].real))

eqns["humn"] = 1j
m1, _, m2 = eqns.pop("root").split()
known = solve(eqns)
c1 = known[m1]
c2 = known[m2]
print("answer_b:", int((c1.real - c2.real) / (c2.imag - c1.imag)))
