from aocd import data

def part_a(n):
    L = [0]
    pos = 0
    for i in range(1, 2017+1):
        pos = 1 + (pos + n) % i
        L.insert(pos, i)
    return L[pos+1]

def part_b(n):
    pos = 0
    i1 = 1
    for i in range(1, 50000000+1):
        pos = 1 + (pos + n) % i
        if pos == 1:
            i1 = i
    return i1

assert part_a(3) == 638
print(part_a(int(data)))  # part a: 1311
print(part_b(int(data)))  # part b: 39170601
