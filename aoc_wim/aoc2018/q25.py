from itertools import combinations

import networkx as nx
from aocd import data


tests = {
    """0,0,0,0
       3,0,0,0
       0,3,0,0
       0,0,3,0
       0,0,0,3
       0,0,0,6
       9,0,0,0
       12,0,0,0""": 2,
    """-1,2,2,0
       0,0,2,-2
       0,0,0,-2
       -1,2,0,0
       -2,-2,-2,2
       3,0,2,-1
       -1,3,2,2
       -1,0,-1,0
       0,2,1,-2
       3,0,0,0""": 4,
    """1,-1,0,1
       2,0,-1,0
       3,2,-1,0
       0,0,3,1
       0,0,-1,-1
       2,3,-2,0
       -2,2,0,0
       2,-2,0,-1
       1,-1,0,-1
       3,2,0,2""": 3,
    """1,-1,-1,-2
       -2,-2,0,1
       0,2,1,3
       -2,3,-2,1
       0,2,3,-2
       -1,-1,1,-2
       0,-2,-1,0
       -2,2,3,-1
       1,2,2,0
       -1,-2,0,-2""": 8,
}


def part_a(data):
    nodes = [tuple(int(n) for n in s.split(",")) for s in data.splitlines()]
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    for node1, node2 in combinations(nodes, 2):
        if sum(abs(x - y) for x, y in zip(node1, node2)) <= 3:
            graph.add_edge(node1, node2)
    return nx.number_connected_components(graph)


for test_data, expected in tests.items():
    assert part_a(test_data) == expected


print("part a:", part_a(data))
