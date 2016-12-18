from aocd import data


test_data = '''
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''.strip()


def parse_data(data):
    d = {}
    for line in data.splitlines():
        words = line.split()
        name = words[0]
        speed = int(words[3])
        time = int(words[6])
        rest = int(words[-2])
        d[name] = speed, time, rest
    return d


def race(data, max_t):
    reindeers = parse_data(data)
    distances = {}
    for name, (speed, time, rest) in reindeers.items():
        t = max_t
        distance = 0
        while t > 0:
            dt = min(time, t)
            distance += dt * speed
            t -= dt
            t -= rest
        distances[name] = distance
    return max(distances.values())


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



assert race(test_data, max_t=1000) == 1120
print(race(data, max_t=2503))  # part a: 2655


def race2(data, max_t):
    deers = [Reindeer(line) for line in data.splitlines()]
    for t in range(max_t):
        for deer in deers:
            deer.step()
        max_distance = max([deer.distance for deer in deers])
        for deer in deers:
            if deer.distance == max_distance:
                deer.points += 1
    print [deer.points for deer in deers]
    return max([deer.points for deer in deers])


assert race2(test_data, max_t=1000) == 689
print(race2(data, max_t=2503))  # part b: 1059

