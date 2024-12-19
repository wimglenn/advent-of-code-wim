"""
--- Day 14: Restroom Redoubt ---
https://adventofcode.com/2024/day/14
"""
from aocd import data
from aocd import extra
from collections import Counter
from dataclasses import dataclass
import math
import parse
import statistics


w = extra.get("width", 101)
h = extra.get("height", 103)


@dataclass
class Bot:
    x: int
    y: int
    dx: int
    dy: int

    @classmethod
    def fromline(cls, line):
        [parsed] = parse.findall("p={:d},{:d} v={:d},{:d}", line)
        return cls(*parsed.fixed)

    def move(self, t=1):
        self.x = (self.x + self.dx * t) % w
        self.y = (self.y + self.dy * t) % h

    @property
    def quadrant(self):
        if self.x == w//2 or self.y == h//2:
            # "Robots that are exactly in the middle (horizontally or vertically) don't
            # count as being in any quadrant"
            return
        return self.x < w//2, self.y < h//2


bots = [Bot.fromline(x) for x in data.splitlines()]
for bot in bots:
    bot.move(100)
quadrants = [bot.quadrant for bot in bots]
quadrant_counts = Counter(quadrants)
del quadrant_counts[None]
a = math.prod(quadrant_counts.values())
print("answer_a:", a)

b = 100
var0 = statistics.pvariance([bot.x + bot.y for bot in bots])
if not extra:
    while True:
        for bot in bots:
            bot.move()
        b += 1
        if statistics.pvariance([bot.x + bot.y for bot in bots]) < var0/2:
            print("answer_b:", b)
            break
