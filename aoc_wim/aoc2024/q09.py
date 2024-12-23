"""
--- Day 9: Disk Fragmenter ---
https://adventofcode.com/2024/day/9
"""
from aocd import data


disk = [*map(int, data)]
offset = disk.pop(0)  # ignore file 0, it can't move and I want to use id 0 for space
for i, val in enumerate(disk):
    f_id = (i + 1) // 2 if i % 2 else 0
    disk[i] = f_id, val
max_f_id = f_id


def checksum(disk):
    i = offset
    result = 0
    for f_id, size in disk:
        result += sum(f_id * (i + j) for j in range(size))
        i += size
    return result


def defrag_a(disk):
    disk = disk.copy()
    while True:
        for i, (f, space) in enumerate(disk):
            if f:
                continue
            f_id, size = disk.pop()
            if f_id == 0:
                break
            if size <= space:
                disk[i:i+1] = (f_id, size), (0, space - size)
                break
            else:
                disk[i] = f_id, space
                disk.append((f_id, size - space))
                break
        else:
            return disk


def defrag_b(disk):
    disk = disk.copy()
    for f_id in range(max_f_id, 0, -1):
        for i, (f, size) in enumerate(reversed(disk)):
            if f == f_id:
                i = len(disk) - 1 - i
                break
        for j, (f, space) in enumerate(disk):
            if not f and space >= size and j < i:
                disk[i] = 0, size
                disk[j:j+1] = (f_id, size), (0, space - size)
                break
    return disk


print("answer_a:", checksum(defrag_a(disk)))
print("answer_b:", checksum(defrag_b(disk)))
