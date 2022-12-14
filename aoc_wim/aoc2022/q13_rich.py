"""
--- Day 13: Distress Signal ---
https://adventofcode.com/2022/day/13
"""
from aocd import data
from json import loads


class Packet:

    def __init__(self, content):
        self.content = content

    def __getitem__(self, index):
        return Packet(self.content[index])

    def __lt__(self, other):
        if not isinstance(other, Packet):
            return NotImplemented
        match self.content, other.content:
            case int(), int():
                if self.content < other.content:
                    return True
                elif other.content < self.content:
                    return False
                # raise NotImplementedError
                return False
            case list(), list():
                for x, y in zip(self, other):
                    if x < y:
                        return True
                    elif y < x:
                        return False
                if len(self.content) < len(other.content):
                    return True
                elif len(other.content) < len(self.content):
                    return False
                # raise NotImplementedError
                return False
            case list(), int():
                return self < Packet([other.content])
            case int(), list():
                return Packet([self.content]) < other

    def __repr__(self):
        return f"Packet({self.content})"


a = 0
i2 = 1
i6 = 2
for i, chunk in enumerate(data.split("\n\n"), 1):
    first, second = [Packet(loads(x)) for x in chunk.split("\n")]
    a += i * (first < second)
    for packet in first, second:
        if packet < Packet([[2]]):
            i2 += 1
            i6 += 1
        elif packet < Packet([[6]]):
            i6 += 1

print("part a:", a)
print("part b:", i2 * i6)
