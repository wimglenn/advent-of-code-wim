import networkx as nx
from aocd import data


def part_a(data):
    g = nx.Graph(x.split(")") for x in data.splitlines())
    return sum(nx.shortest_path_length(g, x, "COM") for x in g.nodes)


def part_b(data):
    g = nx.Graph(x.split(")") for x in data.splitlines())
    return nx.shortest_path_length(g, "YOU", "SAN") - 2


test_a = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

test_b = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""

assert part_a(test_a) == 42
assert part_b(test_b) == 4
print(part_a(data))
print(part_b(data))
