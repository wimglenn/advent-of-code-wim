import re

from aocd import data


def walk(s):
    n_removed = 0
    while "!!" in s:
        s = s.replace("!!", "")
    s = re.sub("!.", "", s)
    n_removed += len(s) - len(re.sub("<.*?>", "", s))
    n_removed -= 2 * len(re.findall("<.*?>", s))
    s = re.sub("<.*?>", "", s)
    score = 0
    nesting = 0
    for c in s:
        if c == "{":
            nesting += 1
        elif c == "}":
            score += nesting
            nesting -= 1
    return score, n_removed


tests = {
    "{}": 1,
    "{{{}}}": 6,
    "{{},{}}": 5,
    "{{{},{},{{}}}}": 16,
    "{<a>,<a>,<a>,<a>}": 1,
    "{{<ab>},{<ab>},{<ab>},{<ab>}}": 9,
    "{{<!!>},{<!!>},{<!!>},{<!!>}}": 9,
    "{{<a!>},{<a!>},{<a!>},{<ab>}}": 3,
}
for k, v in tests.items():
    assert walk(k)[0] == v

tests_b = {
    "<>": 0,
    "<random characters>": 17,
    "<<<<>": 3,
    "<{!>}>": 2,
    "<!!!>>": 0,
    '<{o"i!a,<{i<a>': 10,
}
for k, v in tests_b.items():
    assert walk(k)[1] == v

a, b = walk(data)
print("part a:", a)
print("part b:", b)
