"""
--- Day 7: Recursive Circus ---
https://adventofcode.com/2017/day/7
"""
from collections import Counter
from collections import deque

from aocd import data
from wimpy import cached_property


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


nodes = {}
tree = make_tree(data)
print(tree.name)
print(find_bad_node_correct_weight(tree))
