"""
--- Day 23: Crab Cups ---
https://adventofcode.com/2020/day/23
"""
from aocd import data
from operator import attrgetter


class Cup:

    __slots__ = "label", "r"

    def __init__(self, label, r=None):
        self.label = label
        self.r = r  # the cup clockwise to the right


class CupGame:

    def __init__(self, data, n=None):
        unsorted = len(data)
        labels = [int(x) for x in data.strip()]
        self.maxlabel = max(labels)
        if n is not None:
            labels.extend(range(self.maxlabel + 1, n + 1))
            self.maxlabel = labels[-1]
        cups = self.cups = [Cup(n) for n in labels]
        for i in range(self.maxlabel):
            cups[i-1].r = cups[i]
        self.current = cups[0]
        self.cups[:unsorted] = sorted(self.cups[:unsorted], key=attrgetter("label"))

    def play(self, iterations=1):
        for i in range(iterations):
            label = self.current.label - 1 or self.maxlabel
            pickup_labels = [
                self.current.r.label,
                self.current.r.r.label,
                self.current.r.r.r.label,
            ]
            while label in pickup_labels:
                label = label - 1 or self.maxlabel
            dest = self.cups[label - 1]
            destr = dest.r
            c0 = self.current
            c1 = c0.r
            c3 = c1.r.r
            # cut the circle
            c0.r = c3.r
            # relink after dest
            dest.r = c1
            c3.r = destr
            self.current = self.current.r


game = CupGame(data)
game.play(iterations=100)
cup1 = game.cups[0]
cup = cup1.r
labels = []
while cup is not cup1:
    labels.append(str(cup.label))
    cup = cup.r
print("part a:", "".join(labels))

game = CupGame(data, n=1000000)
game.play(iterations=10000000)
cup1 = game.cups[0]
print("part b:", cup1.r.label * cup1.r.r.label)
