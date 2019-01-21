from aocd import data
from collections import deque
from itertools import count


def parsed(data):
    discs = []
    for line in data.splitlines():
        words = line.split()
        n_pos, pos_t0 = int(words[3]), int(words[-1].rstrip('.'))
        disc = deque(range(n_pos))
        disc.rotate(pos_t0)
        discs.append(disc)
    # MAGIC TRICK: if we initially offset each disc by the position it is 
    # placed from the top of the stack, then we can assume that the capsule 
    # falls through the discs without any delay
    for i, disc in enumerate(discs, 1):
        disc.rotate(i)
    return discs


def find_time(data):
    discs = parsed(data)
    for t in count():
        if not any(disc[0] for disc in discs): 
            return t
        for disc in discs: 
            disc.rotate(1)


test_data = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

assert find_time(test_data) == 5
print(find_time(data))
data += '\nBonus disc has 11 positions; at time=0, it is at position 0.'
print(find_time(data))
