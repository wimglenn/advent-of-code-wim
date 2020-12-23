"""
--- Day 23: Crab Cups ---
https://adventofcode.com/2020/day/23
"""
# data = "562893147"
from aocd import data
from operator import attrgetter


class Cup:

    __slots__ = "label", "left", "right"

    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Cup({self.label})"


class CupGame:

    def __init__(self, data, n=None):
        unsorted = len(data)
        labels = [int(x) for x in data.strip()]
        self.maxlabel = max(labels)
        if n is not None:
            labels.extend(range(self.maxlabel + 1, n + 1))
            self.maxlabel = labels[-1]
        cups = self.cups = [Cup(n) for n in labels]
        for c0, c1 in zip(cups, cups[1:] + cups[:1]):
            c0.right, c1.left = c1, c0
        self.current_cup = cups[0]
        self.cups[:unsorted] = sorted(self.cups[:unsorted], key=attrgetter("label"))
        self.i = 1

    def cup(self, label):
        result = self.current_cup
        while self.current_cup.label != label:
            result = result.left
        return result

    def move(self):
        dest = self.dest()
        rdest = dest.right
        c1, c2, c3 = self.pickup()
        c0 = self.current_cup
        c4 = c3.right
        # cut the circle
        c0.right, c4.left = c4, c0
        # relink after dest
        c1.left, dest.right = dest, c1
        c3.right, rdest.left = rdest, c3
        self.i += 1
        self.current_cup = self.current_cup.right

    def pickup(self):
        return [
            self.current_cup.right,
            self.current_cup.right.right,
            self.current_cup.right.right.right,
        ]

    def dest(self):
        label = self.current_cup.label - 1
        label = label or self.maxlabel
        pickup_labels = [c.label for c in self.pickup()]
        while label in pickup_labels:
            label -= 1
            label = label or self.maxlabel
        dest = self.cups[label - 1]
        return dest

    def pprint(self):
        print(f"-- move {self.i} --")
        cup = self.current_cup
        for i in range(1, self.i):
            cup = cup.left
        print("cups:", end=" ")
        for i in range(1, 10):
            if cup is self.current_cup:
                print(f"({cup.label})", end="")
            else:
                print(str(cup.label).center(3), end="")
            cup = cup.right
        print()
        print("pick up:", ", ".join([str(c.label) for c in self.pickup()]))
        print("destination:", self.dest().label)
        print()


game = CupGame(data)
for i in range(100):
    game.move()

cup1 = game.cups[0]
cup = cup1.right
print("part a: ", end="")
while cup is not cup1:
    print(cup.label, end="")
    cup = cup.right
print()

game = CupGame(data, n=1000000)
for i in range(10000000):
    game.move()
cup1 = game.cups[0]
print("part b:", cup1.right.label * cup1.right.right.label)
