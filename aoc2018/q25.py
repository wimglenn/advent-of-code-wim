from aocd import data
import networkx as nx
from itertools import combinations


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
        if sum(abs(node1[i] - node2[i]) for i in range(4)) <= 3:
            graph.add_edge(node1, node2)
    return len(list(nx.connected_components(graph)))


for text, n in tests.items():
    assert part_a(text) == n

print(part_a(data))  # 375
