"""
--- Day 8: Memory Maneuver ---
https://adventofcode.com/2018/day/8
"""
from anytree import NodeMixin
from aocd import data


class MyNode(NodeMixin):
    def __init__(self, parent=None):
        self.parent = parent

    @property
    def val(self):
        children = self.children
        if len(children) == 0:
            return sum(self.metas)
        else:
            total = 0
            for m in self.metas:
                try:
                    total += children[m - 1].val
                except IndexError:
                    pass
            return total


data = [int(x) for x in data.split()]
sum_all_metas = 0
node = root = MyNode()
try:
    i = 0
    while data:
        if data[i] == 0:
            n_metas = data[i + 1]
            metas = data[i + 2 : i + 2 + n_metas]
            sum_all_metas += sum(metas)
            del data[i : i + 2 + n_metas]
            data[i - 2] -= 1
            i -= 2
            node.metas = metas
            node = node.parent
        else:
            i += 2
            node = MyNode(parent=node)
except IndexError:
    assert node is root
    root.metas = metas
    print("part a:", sum_all_metas)
    print("part b:", node.val)
