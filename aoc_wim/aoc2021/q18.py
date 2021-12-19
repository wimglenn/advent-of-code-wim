"""
--- Day 18: Snailfish ---
https://adventofcode.com/2021/day/18
"""
from aocd import data
from itertools import permutations
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
            if other == 0:
                # this is to allow summing a list of SnailfishNumbers
                return self
            return NotImplemented
        result = SnailfishNumber(f"[{self},{other}]")
        self.parent = other.parent = result
        result.reduce()
        return result

    def __radd__(self, other):
        if other == 0:
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
            action = None
            leaf_nodes = []
            explodable_nodes = []
            splittable_nodes = []
            while stack:
                node, depth = stack.pop()
                if node.leaf:
                    leaf_nodes.append(node)
                    if abs(node) >= 10:
                        splittable_nodes.append(node)
                else:
                    stack.extend([(node.left, depth + 1), (node.right, depth + 1)])
                    if depth == 4 and node.left.leaf and node.right.leaf:
                        explodable_nodes.append(node)
            if not explodable_nodes and not splittable_nodes:
                # reduction is finished
                break

            if explodable_nodes:
                action = "explode"
                node = explodable_nodes[-1]
            else:
                action = "split"
                node = splittable_nodes[-1]

            if action == "split":
                assert node.leaf
                n = abs(node)
                assert n >= 10
                node.left = SnailfishNumber(n // 2, parent=self)
                node.right = SnailfishNumber((n + 1) // 2, parent=self)
                # print("after split:   ", self)
            elif action == "explode":
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
            if action is None:  # reduction finished
                break


ns = [SnailfishNumber(line) for line in data.splitlines()]
print("part a:", abs(sum(ns)))
print("part b:", max([abs(n1 + n2) for n1, n2 in permutations(ns, 2)], default=0))
