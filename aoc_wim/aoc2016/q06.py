from collections import Counter

from aocd import data


test_data = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""


def decode(data, f):
    counters = [Counter(x) for x in zip(*data.splitlines())]
    return "".join(f(c, key=c.get) for c in counters)


assert decode(test_data, f=max) == "easter"
assert decode(test_data, f=min) == "advent"

print(decode(data, f=max))
print(decode(data, f=min))
