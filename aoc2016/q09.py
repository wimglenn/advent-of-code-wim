from aocd import data
from collections import deque


def get_marker(iterator):
    marker = ''
    for c in iterator:
        if c == ')':
            break
        marker += c
    duration, multiplier = [int(n) for n in marker.split('x')]
    length = len(marker) + 2
    return [duration, multiplier, length]


def part1(s):
    result = 0
    iterator = iter(s)
    for c in iterator:
        if c == '(':
            duration, multiplier, _length = get_marker(iterator)
            for _ in range(duration):
                next(iterator)
            result += duration * multiplier
        else:
            result += 1
    return result


def parse(s):
    parsed = deque()
    iterator = iter(s)
    while True:
        letter = next(iterator, None)
        if letter is None:
            break
        if letter == '(':
            parsed.append(get_marker(iterator))
        else:
            parsed.append(1)
    return parsed


def part2(s):
    parsed = parse(s)
    result = 0
    while True:
        try:
            x = parsed.popleft()
        except IndexError:
            break
        if isinstance(x, int):
            result += x
        else:
            duration, multiplier, length = x
            i = 0
            while duration > 0:
                if isinstance(parsed[i], int):
                    duration -= 1
                    parsed[i] *= multiplier
                else:
                    duration -= parsed[i][2]
                i += 1
    return result


assert(part1('ADVENT') == 6)
assert(part1('A(1x5)BC') == 7)  # 1 + 5 + 1
assert(part1('(3x3)XYZ') == 9)  # 3*3
assert(part1('A(2x2)BCD(2x2)EFG') == 11)  # 1 + 2*2 + 1 + 2*2 + 1
assert(part1('(6x1)(1x3)A') == 6)
assert(part1('X(8x2)(3x3)ABCY') == 18)


assert(part2('(3x3)XYZ')) == len('XYZXYZXYZ') == 9  # 3x3
assert(part2('X(8x2)(3x3)ABCY')) == len('XABCABCABCABCABCABCY') == 20  # 1 + 6x3 + 1
assert(part2('(27x12)(20x12)(13x14)(7x10)(1x12)A')) == 241920  # 12 * 12 * 14 * 10 * 12
assert(part2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')) == 445


data = data.strip()
print(part1(data))  # 138735
print(part2(data))  # 11125026826
