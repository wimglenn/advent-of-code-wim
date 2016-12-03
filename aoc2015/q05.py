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


n_nice1 = sum(1 for word in data.splitlines() if is_nice1(word))
n_nice2 = sum(1 for word in data.splitlines() if is_nice2(word))


print(n_nice1)
print(n_nice2)
