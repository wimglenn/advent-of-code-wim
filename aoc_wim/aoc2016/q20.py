"""
--- Day 20: Firewall Rules ---
https://adventofcode.com/2016/day/20
"""
from aocd import data


def cleanup_data(data):
    intervals = []
    for line in data.splitlines():
        left, right = line.split("-")
        interval = int(left), int(right)
        intervals.append(interval)
    intervals.sort()

    while True:
        n = len(intervals)
        for i in range(n - 1):
            lo_p, hi_p = intervals[i]
            lo, hi = intervals[i + 1]
            if lo <= hi_p + 1:
                del intervals[i + 1]
                intervals[i] = lo_p, max(hi_p, hi)
                break
        else:
            break

    return intervals


def part_a(clean_data):
    return clean_data[0][1] + 1


def part_b(clean_data, n_min=0, n_max=4294967295):
    n = n_max - n_min + 1
    for lo, high in clean_data:
        n -= high - lo + 1
    return n


if __name__ == "__main__":
    clean_data = cleanup_data(data)
    print(part_a(clean_data))
    print(part_b(clean_data))
