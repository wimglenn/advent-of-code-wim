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


ns = [int(x) for x in data.split()]
sum_all_metas = 0
node = root = MyNode()
try:
    i = 0
    while ns:
        if ns[i] == 0:
            n_metas = ns[i + 1]
            metas = ns[i + 2 : i + 2 + n_metas]
            sum_all_metas += sum(metas)
            del ns[i : i + 2 + n_metas]
            ns[i - 2] -= 1
            i -= 2
            node.metas = metas
            node = node.parent
        else:
            i += 2
            node = MyNode(parent=node)
except IndexError:
    assert node is root
    root.metas = metas
    print("answer_a:", sum_all_metas)
    print("answer_b:", node.val)
