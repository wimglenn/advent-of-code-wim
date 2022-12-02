"""
--- Day 2: Rock Paper Scissors ---
https://adventofcode.com/2022/day/2
"""
from aocd import data
from enum import Enum
from bidict import bidict
from functools import cached_property


class Shape(Enum):
    A = X = Rock = 1
    B = Y = Paper = 2
    C = Z = Scissors = 3

    @cached_property
    def _lookup(self):
        return bidict({
            Shape.Rock: Shape.Scissors,
            Shape.Scissors: Shape.Paper,
            Shape.Paper: Shape.Rock,
        })

    @property
    def wins_against(self):
        return self._lookup[self]

    @property
    def loses_to(self):
        return self._lookup.inv[self]


def score(glyph_elf, glyph_you, part):
    elfs_shape = Shape[glyph_elf]
    if part == "a":
        your_shape = Shape[glyph_you]
    elif part == "b":
        if glyph_you == "X":  # you should lose
            your_shape = elfs_shape.wins_against
        elif glyph_you == "Y":  # you should draw
            your_shape = elfs_shape
        elif glyph_you == "Z":  # you should win
            your_shape = elfs_shape.loses_to
    if your_shape.loses_to == elfs_shape:
        your_score = your_shape.value + 0
    elif your_shape is elfs_shape:
        your_score = your_shape.value + 3
    elif your_shape.wins_against == elfs_shape:
        your_score = your_shape.value + 6
    return your_score

a = b = 0
for line in data.splitlines():
    elf, me = line.split()
    a += score(elf, me, part="a")
    b += score(elf, me, part="b")

print("part a:", a)
print("part b:", b)
