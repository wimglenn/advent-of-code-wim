from aocd import data


test_data = '211'


def chunker(s):
    group = ''
    it = iter(s)
    for c in it:
        if group:
            if group.endswith(c):
                group += c
            else:
                yield group
                group = c
        else:
            group += c
    if group:
        yield group


def look_and_see_gen(s):
    for chunk in chunker(s):
        yield str(len(chunk))
        yield chunk[0]


def look_and_see(s, n=1):
    for i in range(n):
        s = ''.join(look_and_see_gen(s))
    return s


assert look_and_see(test_data) == '1221'
assert look_and_see('1', n=5) == '312211'

print(len(look_and_see(data, n=40)))  # part a: 252594
print(len(look_and_see(data, n=50)))  # part b: 3579328
