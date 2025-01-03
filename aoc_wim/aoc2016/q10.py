"""
--- Day 10: Balance Bots ---
https://adventofcode.com/2016/day/10
"""
from math import prod

from aocd import data
from aocd import extra
from parse import parse


class Bot:
    def __init__(self, name, low_to=None, high_to=None):
        self.name = name
        self.low_to = low_to
        self.high_to = high_to
        self.chips = []
        self.part_b = False

    def receive(self, chip):
        self.chips.append(chip)
        if len(self.chips) == 2:
            self.send()

    def send(self):
        low, high = sorted(self.chips)
        self.chips = []
        self.low_to.receive(low)
        self.high_to.receive(high)
        if (low, high) == (lo, hi):
            self.part_b = True


receives = []
receivers = {}
lines = data.splitlines()
hi = extra.get("chip1", 61)
lo = extra.get("chip2", 17)
for line in lines:
    if line.startswith("value"):
        tup = parse("value {:d} goes to {}", line).fixed
        receives.append(tup)
    else:
        result = parse("{} gives low to {} and high to {}", line)
        bot_name, low_to, high_to = result.fixed
        bot = receivers.get(bot_name, Bot(bot_name))
        bot.low_to = receivers.get(low_to, Bot(low_to))
        bot.high_to = receivers.get(high_to, Bot(high_to))
        for receiver in bot, bot.low_to, bot.high_to:
            receivers[receiver.name] = receiver

for n, bot_name in receives:
    receivers[bot_name].receive(n)
outputs = [receivers[f"output {o}"].chips for o in (0, 1, 2)]
[bot_a] = [v for v in receivers.values() if v.part_b]
print("answer_a:", int(bot_a.name.lstrip("bot ")))
print("answer_b:", prod([n for [n] in outputs]))
