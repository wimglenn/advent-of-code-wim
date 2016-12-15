from aocd import data
from collections import deque
from itertools import count


test_data = '''Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
'''

def parse_data(text):
    discs = []
    for line in text.splitlines():
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


def find_time(discs):
    for t in count():
        if not any(disc[0] for disc in discs): 
            return t
        for disc in discs: 
            disc.rotate(1)


assert find_time(parse_data(test_data)) == 5

discs_a = parse_data(data)
discs_b = parse_data(data + 'Bonus disc has 11 positions; at time=0, it is at position 0.')

print(find_time(discs_a))  # part A: 317371
print(find_time(discs_b))  # part B: 2080951
