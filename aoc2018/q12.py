from aocd import data


test_data = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""


def parsed(data):
    initial, _, *rest = data.splitlines()
    s0 = initial.split()[-1]
    p0 = s0.index("#")
    s0 = s0.strip(".")
    rules = {r.split()[0] for r in rest if r.endswith("#")}
    return s0, p0, rules


def mutate(s, p0, rules):
    s = '....' + s + '....'
    chunks = [s[i:i+5] for i in range(len(s))]
    full = ''.join(["#" if c in rules else "." for c in chunks])
    p0 += full.index("#") - 2
    return full.strip("."), p0


def score(s, p0=0):
    return sum(i for i,v in  enumerate(s, start=p0) if v == "#")


def run(data, n=20):
    s0, p0, rules = parsed(data)
    for i in range(n):
        s1, p1 = mutate(s0, p0, rules)
        if s1 == s0:
            return score(s1, p0=p1+n-i-1)
        s0, p0 = s1, p1
    return score(s0, p0)


assert run(test_data) == 325
part_a = run(data)
print(part_a)  # 2040

part_b = run(data, n=50000000000)
print(part_b)  # 1700000000011
