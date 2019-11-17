from aocd import data


def vowel_count(s):
    vowels = set("aeiou")
    return sum(1 for c in s if c in vowels)


def has_double(s):
    for left, right in zip(s[:-1], s[1:]):
        if left == right:
            return True


def blacklisted(s):
    for substring in "ab", "cd", "pq", "xy":
        if substring in s:
            return True


def has_pair(s):
    for left, right in zip(s[:-1], s[1:]):
        if s.count(left + right) > 1:
            return True


def has_skip_repeat(s):
    for left, right in zip(s[:-2], s[2:]):
        if left == right:
            return True


def is_nice_a(s):
    return vowel_count(s) >= 3 and has_double(s) and not blacklisted(s)


def is_nice_b(s):
    return has_pair(s) and has_skip_repeat(s)


assert is_nice_a("ugknbfddgicrmopn")
assert is_nice_a("aaa")
assert not is_nice_a("jchzalrnumimnmhp")
assert not is_nice_a("haegwjzuvuyypxyu")
assert not is_nice_a("dvszwmarrgswjxmb")
assert is_nice_b("qjhvhtzxzqqjkmpb")
assert is_nice_b("xxyxx")
assert not is_nice_b("uurcxstgmygtbstg")
assert not is_nice_b("ieodomkazucvgmuy")

words = data.splitlines()
print("part a:", len([w for w in words if is_nice_a(w)]))
print("part b:", len([w for w in words if is_nice_b(w)]))
