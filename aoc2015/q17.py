from aocd import data
from collections import Counter


test_data = '''
20
15
10
5
5
'''.strip()


def ways(total=25, containers=(5,5,10,15,20)):

    memo = {}

    def worker(hand=frozenset()):
        if hand not in memo:
            sum_ = sum(containers[i] for i in hand)
            if sum_ == total:
                result = {hand}
            elif sum_ > total:
                result = set()
            else:
                choices = set(range(len(containers))) - hand
                hands = (worker(hand | {choice}) for choice in choices)
                result = set.union(*hands)
            memo[hand] = result
        return memo[hand]

    result = [[containers[i] for i in way] for way in set(worker())]
    return result


def part_a(data, total=150):
    containers = [int(n) for n in data.splitlines()]
    return len(ways(total=total, containers=containers))

def part_b(data, total=150):
    containers = [int(n) for n in data.splitlines()]
    all_ways = ways(total=total, containers=containers)
    min_len = min([len(way) for way in all_ways])
    return sum(1 for way in all_ways if len(way) == min_len)


assert part_a(test_data, total=25) == 4
print(part_a(data))  # 1638

assert part_b(test_data, total=25) == 3
print(part_b(data))  # 17
