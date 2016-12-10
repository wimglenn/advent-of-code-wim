from aocd import data


class Bot(object):
    def __init__(self, name, low_to=None, high_to=None):
        self.name = name
        self.low_to = low_to
        self.high_to = high_to
        self.chips = []

    def receive(self, chip):
        self.chips.append(chip)
        if len(self.chips) == 2:
            self.send()

    def send(self):
        low, high = sorted(self.chips)
        if (low, high) == (17, 61):
            print(self.name)
        self.chips = []
        self.low_to.receive(low)
        self.high_to.receive(high)


receives = []
receivers = {}

for line in data.splitlines():
    if line.startswith('value'):
        # value N goes to bot B
        val = int(line.split()[1])
        bot_name = line.partition(' goes to ')[-1]
        receives.append((val, bot_name))
    else:
        # bot 0 gives low to output 2 and high to output 0
        bot_name, _, after = line.partition(' gives low to ')
        low_to, _, high_to = after.partition(' and high to ')
        bot = receivers.get(bot_name, Bot(bot_name))
        bot.low_to = receivers.get(low_to, Bot(low_to))
        bot.high_to = receivers.get(high_to, Bot(high_to))
        for receiver in bot, bot.low_to, bot.high_to:
            receivers[receiver.name] = receiver

for n, bot_name in receives:
    receivers[bot_name].receive(n)

n = 1
for o in 0, 1, 2:
    n *= receivers['output {}'.format(o)].chips.pop()

print(n)
