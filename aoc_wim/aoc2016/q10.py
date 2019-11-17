from aocd import data
from parse import parse

from ..stuff import prod


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


def parsed(data, lh=(17, 61)):
    receives = []
    receivers = {}
    for line in data.splitlines():
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
    return receives, receivers


def part_ab(data, lh=(17, 61)):
    receives, receivers = parsed(data, lh=lh)
    for n, bot_name in receives:
        receivers[bot_name].receive(n)
    outputs = [receivers[f"output {o}"].chips for o in (0, 1, 2)]
    [bot_a] = [v for v in receivers.values() if v.part_b]
    a = int(bot_a.name.lstrip("bot "))
    b = prod([n for [n] in outputs])
    return a, b


test_data = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""

assert part_ab(test_data, lh=(2, 5))[0] == 2

a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
