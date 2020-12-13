"""
--- Day 13: Shuttle Search ---
https://adventofcode.com/2020/day/13
"""
from aocd import data

t0, table = data.splitlines()
t0 = int(t0)
buses = [(i, int(b)) for i, b in enumerate(table.split(",")) if b != "x"]
wait, bus = min([(-t0 % b, b) for _, b in buses])
print("part a:", wait * bus)

timestamp = 0
increment = 1
synced = {}
while len(synced) < len(buses):
    timestamp += increment
    for phase, bus in buses:
        if bus not in synced:
            if (timestamp + phase) % bus == 0:
                increment *= bus
                synced[bus] = timestamp
print("part b:", timestamp)
