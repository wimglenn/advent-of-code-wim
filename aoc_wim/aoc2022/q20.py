"""
--- Day 20: Grove Positioning System ---
https://adventofcode.com/2022/day/20
"""
from aocd import data


# doubly-linked list node
class Node:
    __slots__ = "val", "right", "left"

    def __init__(self, val, right=None, left=None):
        self.val = val
        self.right = right
        self.left = left

    def move(self, dist):
        other = self
        dist %= N - 1
        if dist == 0:
            # print(f"{self.val} does not move:")
            return
        for _ in range(dist):
            other = other.right
        left, right = other, other.right
        # print(f"{self.val} moves between {left.val} and {right.val}:")
        self.left.right, self.right.left = self.right, self.left
        left.right = right.left = self
        self.right = right
        self.left = left


def linked_list(numbers):
    nodes = [Node(n) for n in numbers]
    for na, nb in zip(nodes, nodes[1:] + [nodes[0]]):
        na.right = nb
        nb.left = na
    return nodes


numbers = [int(n) for n in data.split()]
N = len(numbers)
nodes = linked_list(numbers)
for node in nodes:
    node.move(dist=node.val)


def sum_of_grove_coordinates(nodes):
    n0 = nodes[numbers.index(0)]
    result = 0
    for _ in range(3):
        for i in range(1000 % N):
            n0 = n0.right
        result += n0.val
    return result


print("part a:", sum_of_grove_coordinates(nodes))

key = 811589153
nodes = linked_list([n * key for n in numbers])
for _ in range(10):
    for node in nodes:
        node.move(dist=node.val)
print("part b:", sum_of_grove_coordinates(nodes))
