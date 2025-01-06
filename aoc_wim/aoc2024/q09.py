"""
--- Day 9: Disk Fragmenter ---
https://adventofcode.com/2024/day/9
"""
from collections import defaultdict
from collections import deque
from dataclasses import dataclass
from heapq import heappop
from heapq import heappush

from aocd import data


@dataclass
class Mem:
    id: int
    pos: int
    size: int

    @property
    def checksum(self):
        return self.id * (2 * self.pos + self.size - 1) * self.size // 2

    def __lt__(self, other):
        if not isinstance(other, Mem):
            return NotImplemented
        return self.pos < other.pos


def parsed(data):
    disk = deque(), deque()
    pos = 0
    for i, size in enumerate(map(int, data)):
        fid, i = divmod(i, 2)
        if size:
            disk[i].append(Mem(fid, pos, size))
        pos += size
    return disk


def defrag_a(data):
    files, free = parsed(data)
    while free[0].pos <= files[-1].pos:
        s = free.popleft()
        f = files.pop()
        if f.size <= s.size:
            f.pos = s.pos
            files.appendleft(f)
            s.size -= f.size
            s.pos += f.size
            if s.size:
                free.appendleft(s)
        else:
            files.append(Mem(f.id, f.pos, f.size - s.size))
            f.pos = s.pos
            f.size = s.size
            files.appendleft(f)
    return sum(f.checksum for f in files)


def defrag_b(data):
    files, free = parsed(data)
    heaps = defaultdict(list)
    for f in free:
        heappush(heaps[f.size], Mem(0, f.pos, f.size))

    for f in reversed(files):
        slots = [h for s, h in heaps.items() if s >= f.size and h and h[0].pos < f.pos]
        if not slots:
            continue
        heap = min(slots, key=lambda h: h[0].pos)
        s = heappop(heap)
        f.pos = s.pos
        s.size -= f.size
        s.pos += f.size
        heappush(heaps[s.size], s)
    return sum(f.checksum for f in files)


print("answer_a:", defrag_a(data))
print("answer_b:", defrag_b(data))
