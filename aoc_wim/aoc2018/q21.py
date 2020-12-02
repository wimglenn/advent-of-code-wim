"""
--- Day 21: Chronal Conversion ---
https://adventofcode.com/2018/day/21
"""
from aocd import data
from parse import parse

template = """\
#ip {:d}
seti {:d} {:d} {:d}
bani {:d} {:d} {:d}
eqri {:d} {:d} {:d}
addr {:d} {:d} {:d}
seti {:d} {:d} {:d}
seti {:d} {:d} {:d}
bori {:d} {:d} {:d}
seti {bignum:d} {:d} {:d}
bani {:d} {:d} {:d}
addr {:d} {:d} {:d}
bani {:d} {:d} {:d}
muli {:d} {prime:d} {:d}
bani {:d} {:d} {:d}
gtir {:d} {:d} {:d}
addr {:d} {:d} {:d}
addi {:d} {:d} {:d}
seti {:d} {:d} {:d}
seti {:d} {:d} {:d}
addi {:d} {:d} {:d}
muli {:d} {:d} {:d}
gtrr {:d} {:d} {:d}
addr {:d} {:d} {:d}
addi {:d} {:d} {:d}
seti {:d} {:d} {:d}
addi {:d} {:d} {:d}
seti {:d} {:d} {:d}
setr {:d} {:d} {:d}
seti {:d} {:d} {:d}
eqrr {:d} {:d} {:d}
addr {:d} {:d} {:d}
seti {:d} {:d} {:d}"""
parsed = parse(template, data)


part_a = part_b = None
seen = set()
r3 = 0x10000
r5 = parsed.named["bignum"]
while True:
    r5 += r3 & 0xFF
    r5 &= 0xFFFFFF
    r5 *= parsed.named["prime"]
    r5 &= 0xFFFFFF
    if r3 >= 256:
        r3 //= 256
        continue
    if part_a is None:
        part_a = r5
    if r5 in seen:
        break
    part_b = r5
    seen.add(r5)
    r3 = r5 | 0x10000
    r5 = parsed.named["bignum"]

print(part_a)
print(part_b)
