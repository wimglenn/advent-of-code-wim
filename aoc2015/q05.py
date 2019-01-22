from aocd import data


def vowel_count(s):
    vowels = set('aeiou')
    return sum(1 for c in s if c in vowels)


def has_double(s):
    for left, right in zip(s[:-1], s[1:]):
        if left == right:
            return True


def blacklisted(s):
    for substring in 'ab', 'cd', 'pq', 'xy':
        if substring in s:
            return True


def is_nice1(s):
    return vowel_count(s) >= 3 and has_double(s) and not blacklisted(s)


def has_pair(s):
    for left, right in zip(s[:-1], s[1:]):
        if s.count(left + right) > 1:
            return True


def has_skip_repeat(s):
    for left, right in zip(s[:-2], s[2:]):
        if left == right:
            return True


def is_nice2(s):
    return has_pair(s) and has_skip_repeat(s)


def part_a(data):
    return sum(1 for word in data.splitlines() if is_nice1(word))


def part_b(data):
    return sum(1 for word in data.splitlines() if is_nice2(word))


assert is_nice1("ugknbfddgicrmopn")
assert is_nice1("aaa")
assert not is_nice1("jchzalrnumimnmhp")
assert not is_nice1("haegwjzuvuyypxyu")
assert not is_nice1("dvszwmarrgswjxmb")
assert is_nice2("qjhvhtzxzqqjkmpb")
assert is_nice2("xxyxx")
assert not is_nice2("uurcxstgmygtbstg")
assert not is_nice2("ieodomkazucvgmuy")


print("part a:", part_a(data))
print("part b:", part_b(data))
