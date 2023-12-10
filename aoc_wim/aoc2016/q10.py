"""
--- Day 10: Balance Bots ---
https://adventofcode.com/2016/day/10
"""
from math import prod

from aocd import data
from parse import parse


class Bot(object):
    def __init__(self, name, low_to=None, high_to=None, lh=(17, 61)):
        self.name = name
        self.low_to = low_to
        self.high_to = high_to
        self.chips = []
        self.part_b = False
        self.lh = lh

    def receive(self, chip):
        self.chips.append(chip)
        if len(self.chips) == 2:
            self.send()

    def send(self):
        low, high = sorted(self.chips)
        self.chips = []
        self.low_to.receive(low)
        self.high_to.receive(high)
        if (low, high) == self.lh:
            self.part_b = True


receives = []
receivers = {}
lines = data.splitlines()
lh = (2, 5) if len(lines) == 6 else (17, 61)
for line in lines:
    if line.startswith("value"):
        tup = parse("value {:d} goes to {}", line).fixed
        receives.append(tup)
    else:
        result = parse("{} gives low to {} and high to {}", line)
        bot_name, low_to, high_to = result.fixed
        bot = receivers.get(bot_name, Bot(bot_name, lh=lh))
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
