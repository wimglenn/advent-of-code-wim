import networkx as nx
from aocd import data


def parsed(data):
    graph = nx.Graph()
    for line in data.replace(" <->", ",").splitlines():
        n0, *nodes = [int(n) for n in line.split(", ")]
        graph.add_node(n0)
        for node in nodes:
            graph.add_edge(n0, node)
    return graph


def part_ab(data):
    graph = parsed(data)
    [a] = [len(g) for g in nx.connected_components(graph) if 0 in g]
    b = nx.number_connected_components(graph)
    return a, b


test_data = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

assert part_ab(test_data) == (6, 2)

a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
