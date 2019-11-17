from collections import Counter
from datetime import timedelta
from operator import attrgetter

from aocd import data
from parse import parse


test_data = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""


class Guard:

    template = "[{t:ti}] Guard #{id:d} begins shift"
    eventstr = "[{t:ti}] {event}"

    def __init__(self, id, began_shift):
        self.id = id
        self.began_shift = began_shift
        self.t0 = None
        self.minutes_asleep = []

    @classmethod
    def from_line(cls, line):
        parsed = parse(cls.template, line)
        return Guard(id=parsed["id"], began_shift=parsed["t"])

    def event(self, line):
        parsed = parse(self.eventstr, line)
        t = parsed["t"]
        if parsed["event"] == "falls asleep":
            self.t0 = t
        elif parsed["event"] == "wakes up":
            t0 = self.t0
            while t0 < t:
                self.minutes_asleep.append(t0.minute)
                t0 += timedelta(minutes=1)
            self.t0 = None

    @property
    def total_sleep_time(self):
        return len(self.minutes_asleep)

    @property
    def sleepiest_minute(self):
        counter = Counter(self.minutes_asleep)
        return max(counter, key=counter.get)

    @property
    def sleepiest_minute_count(self):
        return max(Counter(self.minutes_asleep).values(), default=0)


def part_ab(data):
    guards = {}
    for line in sorted(data.splitlines()):
        if "Guard" in line:
            guard = Guard.from_line(line)
            guard = guards.get(guard.id) or guard
            guards[guard.id] = guard
            continue
        guard.event(line)

    g = max(guards.values(), key=attrgetter("total_sleep_time"))
    part_a = g.id * g.sleepiest_minute
    g = max(guards.values(), key=attrgetter("sleepiest_minute_count"))
    part_b = g.id * g.sleepiest_minute
    return part_a, part_b


assert part_ab(test_data) == (240, 4455)


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
