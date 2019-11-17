import networkx as nx
from aocd import data


tests = {
    # my examples
    "^(N|S|E|W)$": 1,
    "^(N|S|E|W)(N|S|E|W)$": 2,
    "^(N|S|E|W)(N|E|W|S)(W|E|N|S)$": 3,
    "^E(NN|S)E$": 4,
    "^(N|S)N$": 2,
    "^EEE(NN|SSS)EEE$": 9,
    # AoC examples
    "^WNE$": 3,
    "^ENWWW(NEEE|SSE(EE|N))$": 10,
    "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$": 18,
    "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$": 23,
    "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$": 31,
}
steps = dict(zip("NSEW", [-2j, 2j, 2, -2]))
dzs = [
    -1j - 1,
    -1j,
    -1j + 1,
    -1,
    1,
    +1j - 1,
    +1j,
    +1j + 1,
]


def render(g):
    if isinstance(g, str):
        g = graph(g)
    xs = [int(z.real) for z in g.nodes]
    ys = [int(z.imag) for z in g.nodes]
    x0, x1 = min(xs) - 1, max(xs) + 2
    y0, y1 = min(ys) - 1, max(ys) + 2
    for y in range(y0, y1):
        line = ""
        for x in range(x0, x1):
            z = complex(x, y)
            if z == 0:
                line += "X"
            elif z in g.nodes:
                line += "."
            elif (z - 1, z + 1) in g.edges:
                line += "|"
            elif (z - 1j, z + 1j) in g.edges:
                line += "-"
            elif any(z + dz in g.nodes for dz in dzs):
                line += "#"
            else:
                line += " "
        print(line)
    print()


def graph(data, z0=0):
    g = nx.Graph()
    g.add_node(z0)
    tails = [z0]
    stack = []
    for s in data[1:-1]:
        if s in steps:
            dz = steps[s]
            tails[:] = [z + dz for z in tails]
            for z in tails:
                g.add_edge(z - dz, z)
        elif s == "(":
            stack.append(tails)
            new_tails = tails = tails.copy()
        elif s == "|":
            new_tails.extend(tails)
            tails = stack[-1].copy()
        elif s == ")":
            new_tails.extend(tails)
            stack.pop()
            tails = [*dict.fromkeys(new_tails)]
    return g


def part_ab(data):
    g = graph(data)
    distances = [nx.shortest_path_length(g, 0, x) for x in g.nodes]
    part_a = max(distances)
    part_b = sum(1 for d in distances if d >= 1000)
    return part_a, part_b


for test, expected in tests.items():
    a, _b = part_ab(test)
    assert a == expected


render(data)
a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
