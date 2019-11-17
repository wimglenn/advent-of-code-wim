from collections import Counter
from collections import deque

from aocd import data
from wimpy import cached_property

test_data = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

nodes = {}


class Node:
    def __init__(self, name):
        self.name = name
        self.weight = None
        self.parent = None
        self.children = []

    @cached_property
    def rweight(self):
        return self.weight + sum(x.rweight for x in self.children)

    @property
    def siblings(self):
        if self.parent is None:
            return []
        return [x for x in self.parent.children if x is not self]

    @classmethod
    def get_or_create(cls, name):
        if name not in nodes:
            nodes[name] = cls(name)
        return nodes[name]


def make_tree(data):
    for line in data.splitlines():
        line = line.translate(str.maketrans("", "", "()->,"))
        name, weight, *child_names = line.split()
        node = Node.get_or_create(name)
        node.weight = int(weight)
        for name in child_names:
            child = Node.get_or_create(name)
            child.parent = node
            node.children.append(child)
    # find root
    while node.parent:
        node = node.parent
    return node


def find_bad_node_correct_weight(tree):
    d = deque([tree])
    while d:
        node = d.pop()
        c = Counter(x.rweight for x in node.children)
        for child in node.children:
            if c[child.rweight] == 1:
                d.append(child)
                break
    delta = node.rweight - node.siblings[0].rweight
    return node.weight - delta


test_tree = make_tree(test_data)
assert test_tree.name == "tknk"
assert find_bad_node_correct_weight(test_tree) == 60

nodes.clear()
tree = make_tree(data)
print(tree.name)
print(find_bad_node_correct_weight(tree))
