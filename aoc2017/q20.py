from aocd import data
from collections import defaultdict
from parse import parse
from wimpy import chunks

test_data_a = """\
p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>
"""

test_data_b = """\
p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>
"""

template = 'p=<{:d},{:d},{:d}>, v=<{:d},{:d},{:d}>, a=<{:d},{:d},{:d}>'


def parsed(data):
    return [list(parse(template, line).fixed) for line in data.splitlines()]


def key(p):
    return [abs(x) + abs(y) + abs(z) for x, y, z in chunks(reversed(p), 3)]


def part_a(data):
    particles = parsed(data)
    p_min = min(particles, key=key)
    return particles.index(p_min)


def part_b(data):
    particles = parsed(data)
    for _ in range(100):
        d = defaultdict(list)
        for i, p in enumerate(particles):
            d[p[0], p[1], p[2]].append(i)
        kill = set()
        for k, v in d.items():
            if len(v) > 1:
                kill |= set(v)
        for k in sorted(kill, reverse=True):
            del particles[k]
        for p in particles:
            # accelerate
            p[3] += p[6]
            p[4] += p[7]
            p[5] += p[8]
            # translate
            p[0] += p[3]
            p[1] += p[4]
            p[2] += p[5]
    return len(particles)


assert part_a(test_data_a) == 0
assert part_b(test_data_b) == 1

print(part_a(data))
print(part_b(data))
