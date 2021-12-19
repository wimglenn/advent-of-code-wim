"""
--- Day 18: Snailfish ---
https://adventofcode.com/2021/day/18
"""
from aocd import data
import json


class SnailfishNumber:
    """shh, it's really a binary tree"""

    def __init__(self, val, parent=None):
        self.parent = parent
        if isinstance(val, str):
            val = json.loads(val)
        if isinstance(val, int):
            self.left = self.right = None
            self._magnitude = val
        else:
            left, right = val
            if not isinstance(left, SnailfishNumber):
                left = SnailfishNumber(left, parent=self)
            if not isinstance(right, SnailfishNumber):
                right = SnailfishNumber(right, parent=self)
            self.left = left
            self.right = right

    def __abs__(self):
        if self.left is self.right is None:
            return self._magnitude
        return 3 * abs(self.left) + 2 * abs(self.right)

    def __add__(self, other):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented
        result = SnailfishNumber(f"[{self},{other}]")
        self.parent = other.parent = result
        result.reduce()
        return result

    def __radd__(self, other):
        if other == 0:
            # this is to allow summing a homogeneous list of SnailfishNumbers
            return self
        return NotImplemented

    def __str__(self):
        if self.leaf:  # regular number
            return str(abs(self))
        return f"[{self.left},{self.right}]"

    def __eq__(self, other):
        if not isinstance(other, SnailfishNumber):
            return NotImplemented
        return str(self) == str(other)

    @property
    def leaf(self):
        return self.left is self.right is None

    def reduce(self):
        # "explode": prune nodes at depth >= 4
        # "split": grow new nodes at values >= 10
        while True:
            stack = [(self, 0)]
            leaf_nodes = []
            explode = split = None
            while stack:
                node, depth = stack.pop()
                if node.leaf:
                    leaf_nodes.append(node)
                    if abs(node) >= 10:
                        split = node
                else:
                    stack.extend([(node.left, depth + 1), (node.right, depth + 1)])
                    if depth == 4 and node.left.leaf and node.right.leaf:
                        explode = node
            if explode:
                node = explode
                assert not node.leaf
                # Exploding pairs will always consist of two regular numbers.
                assert node.left.leaf and node.right.leaf
                # distribute pair values into prev and next leaf nodes, if any
                for i, n in enumerate(leaf_nodes):
                    if node.right is n:
                        if i > 0:
                            next_leaf = leaf_nodes[i - 1]
                            next_leaf._magnitude += abs(node.right)
                    if node.left is n:
                        if i + 1 < len(leaf_nodes):
                            prev_leaf = leaf_nodes[i + 1]
                            prev_leaf._magnitude += abs(node.left)
                # convert current node into a leaf
                node._magnitude = 0
                node.left = node.right = None
                # print("after explode: ", self)
            elif split:
                node = split
                assert node.leaf
                n = abs(node)
                assert n >= 10
                node.left = SnailfishNumber(n // 2, parent=self)
                node.right = SnailfishNumber((n + 1) // 2, parent=self)
                # print("after split:   ", self)
            else:  # reduction is finished
                break


ns = [SnailfishNumber(line) for line in data.splitlines()]
print("part a:", abs(sum(ns)))
print("part b:", max([abs(n1 + n2) for n1 in ns for n2 in ns], default=0))
