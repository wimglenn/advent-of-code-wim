from aocd import data
from collections import defaultdict
from parse import parse
import numpy as np

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

def get_particles(data):
    particles = {}
    for i, line in enumerate(data.splitlines()):
        parsed = parse('p=<{px:d},{py:d},{pz:d}>, v=<{vx:d},{vy:d},{vz:d}>, a=<{ax:d},{ay:d},{az:d}>', line)
        p = np.array([parsed.named['px'], parsed.named['py'], parsed.named['pz']], dtype=int)
        v = np.array([parsed.named['vx'], parsed.named['vy'], parsed.named['vz']], dtype=int)
        a = np.array([parsed.named['ax'], parsed.named['ay'], parsed.named['az']], dtype=int)
        particles[i] = p,v,a
    return particles

def part_a(data):
    particles = get_particles(data)
    return min(particles, key=lambda i: np.linalg.norm(particles[i][2]))

def part_b(data):
    particles = get_particles(data)
    for _ in range(100):
        d = defaultdict(list)
        for i, (p,v,a) in particles.items():
            d[tuple(p)].append(i)
        kill = set()
        for k,v in d.items():
            if len(v) > 1:
                kill |= set(v)
        for k in kill:
            del particles[k]
        for i, (p,v,a) in list(particles.items()):
            v += a
            p += v
            particles[i] = p,v,a
    return len(particles)

assert part_a(test_data_a) == 0
assert part_b(test_data_b) == 1

print(part_a(data))
print(part_b(data))
