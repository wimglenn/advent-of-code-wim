from aocd import data
import networkx as nx


tests = {
    "^WNE$": 3,
    "^ENWWW(NEEE|SSE(EE|N))$": 10,
    "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$": 18,
    "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$": 23,
    "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$": 31,
}
dirs = dict(zip("NSEW", [-2j, 2j, 2, -2]))


def graph(data):
    x0 = 0
    g = nx.Graph()
    g.add_node(x0)
    branches = []
    for c in data[1:-1]:
        if c in dirs:
            x1 = x0 + dirs[c]
            g.add_edge(x0, x1)
            x0 = x1
        elif c == "(":
            branches.append(x0)
        elif c == "|":
            x0 = branches[-1]
        elif c == ")":
            branches.pop()
    return g


def solve(data):
    g = graph(data)
    distances = [nx.shortest_path_length(g, 0, x) for x in g.nodes]
    part_a = max(distances)
    part_b = sum(1 for d in distances if d >= 1000)
    return part_a, part_b


for test, expected in tests.items():
    part_a, _part_b = solve(test)
    assert part_a == expected


a, b = solve(data)
print(a)  # 3465
print(b)  # 7956
