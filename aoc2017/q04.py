from aocd import data

a = b = 0
for line in data.splitlines():
    words = line.split()
    if len(words) == len(set(words)):
        a += 1
    words = [''.join(sorted(x)) for x in words]
    if len(words) == len(set(words)):
        b += 1

print(a)  # part a: 325
print(b)  # part b: 119
