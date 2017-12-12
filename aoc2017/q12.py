from aocd import data

test_data = '''0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5'''

def run(data):
    d = {}
    for line in data.replace(' <->', ',').splitlines():
        xs = [int(x) for x in line.split(', ')]
        d[tuple(xs)] = set(xs)

    while True:
        for tuple_, set1 in d.items():
            try:
                match = next(k for k, set2 in d.items() if k != tuple_ and set1 & set2)
            except StopIteration:
                # no match for this key - keep looking
                continue
            else:
                # merging match and set1
                d[tuple_] = set1 | d.pop(match)
                break
        else:
            # no match for any key - we are done!
            break

    [set0] = [v for v in d.values() if 0 in v]
    a = len(set0)
    b = len(d)
    return a, b

assert run(test_data) == (6, 2)

a, b = run(data)
print(a)  # part a: 152
print(b)  # part b: 186
