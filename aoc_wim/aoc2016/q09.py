from collections import deque

from aocd import data


def get_marker(iterator):
    marker = ""
    for c in iterator:
        if c == ")":
            break
        marker += c
    duration, multiplier = [int(n) for n in marker.split("x")]
    length = len(marker) + 2
    return [duration, multiplier, length]


def part_a(s):
    result = 0
    iterator = iter(s)
    for c in iterator:
        if c == "(":
            duration, multiplier, _length = get_marker(iterator)
            for _ in range(duration):
                next(iterator)
            result += duration * multiplier
        else:
            result += 1
    return result


def parsed(data):
    d = deque()
    iterator = iter(data.strip())
    while True:
        letter = next(iterator, None)
        if letter is None:
            break
        if letter == "(":
            d.append(get_marker(iterator))
        else:
            d.append(1)
    return d


def part_b(data):
    d = parsed(data)
    result = 0
    while True:
        try:
            x = d.popleft()
        except IndexError:
            break
        if isinstance(x, int):
            result += x
        else:
            duration, multiplier, length = x
            i = 0
            while duration > 0 and i < len(d):
                if isinstance(d[i], int):
                    duration -= 1
                    d[i] *= multiplier
                else:
                    duration -= d[i][2]
                i += 1
    return result


assert part_a("ADVENT") == 6
assert part_a("A(1x5)BC") == 7  # 1 + 5 + 1
assert part_a("(3x3)XYZ") == 9  # 3*3
assert part_a("A(2x2)BCD(2x2)EFG") == 11  # 1 + 2*2 + 1 + 2*2 + 1
assert part_a("(6x1)(1x3)A") == 6
assert part_a("X(8x2)(3x3)ABCY") == 18


assert part_b("(3x3)XYZ") == len("XYZXYZXYZ") == 9  # 3x3
assert part_b("X(8x2)(3x3)ABCY") == len("XABCABCABCABCABCABCY") == 20  # 1 + 6x3 + 1
assert part_b("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920  # 12 * 12 * 14 * 10 * 12
assert part_b("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445

# TODO:
# Additional test cases from AoC author:
# https://www.reddit.com/r/adventofcode/comments/5hh56d/help_dont_understand_puzzle_9_part_b/db0aggl
assert part_b("AAA(4x3)BBB") == len("AAABBBBBBBBB") == 12
# assert part_b('(7x2)A(3x2)BCD') == len('ABA(BABCDBCD') == 12, part_b('(7x2)A(3x2)BCD')

print("part a:", part_a(data))
print("part b:", part_b(data))
