from aocd import data
from itertools import groupby


def look_and_see(s, n=1):
    for i in range(n):
        s = ''.join([f"{len(list(group))}{key}" for key, group in groupby(s)])
    return s


assert look_and_see("211") == '1221'
assert look_and_see('1', n=5) == '312211'

a = look_and_see(data, n=40)
print(len(a))

b = look_and_see(a, n=50-40)
print(len(b))
