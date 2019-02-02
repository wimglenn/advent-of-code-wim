from aocd import data


def has_dupe(txt):
    parts = txt.split()
    return len(parts) != len(set(parts))


def has_anagram(txt):
    parts = [tuple(sorted(x)) for x in txt.split()]
    return len(parts) != len(set(parts))


assert not has_dupe("aa bb cc dd ee")
assert has_dupe("aa bb cc dd aa")
assert not has_dupe("aa bb cc dd aaa")

assert not has_anagram("abcde fghij")
assert has_anagram("abcde xyz ecdab")
assert not has_anagram("a ab abc abd abf abj")
assert not has_anagram("iiii oiii ooii oooi oooo")
assert has_anagram("oiii ioii iioi iiio")


a = b = 0
for txt in data.splitlines():
    a += not has_dupe(txt)
    b += not has_anagram(txt)

print("part a:", a)
print("part b:", b)
