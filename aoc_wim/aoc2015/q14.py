"""
--- Day 14: Reindeer Olympics ---
https://adventofcode.com/2015/day/14
"""
from aocd import data


class Reindeer(object):
    def __init__(self, line):
        words = line.split()
        self.name = words[0]
        self.run_speed = int(words[3])
        self.stamina = int(words[6])
        self.rest_time = int(words[-2])
        self.distance = 0
        self.points = 0
        self.speed = self.run_speed
        self.dt = self.stamina

    def step(self):
        self.distance += self.speed
        self.dt -= 1
        if self.dt == 0:
            if self.speed == 0:
                self.speed = self.run_speed
                self.dt = self.stamina
            else:
                self.speed = 0
                self.dt = self.rest_time


def race(data, max_t, measure):
    deers = [Reindeer(line) for line in data.splitlines()]
    for t in range(max_t):
        for deer in deers:
            deer.step()
        max_distance = max([deer.distance for deer in deers])
        for deer in deers:
            if deer.distance == max_distance:
                deer.points += 1
    return max([getattr(deer, measure) for deer in deers])


if __name__ == "__main__":
    print(race(data, max_t=2503, measure="distance"))
    print(race(data, max_t=2503, measure="points"))
