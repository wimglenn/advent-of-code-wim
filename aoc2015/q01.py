from aocd import data


direction = {'(': +1, ')': -1}

basement = None
floor = 0
for i, c in enumerate(data, 1):
    floor += direction[c]
    if basement is None and floor == -1:
        basement = i


print(floor)
print(basement)
