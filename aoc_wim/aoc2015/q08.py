from aocd import data


test_data = r'''""
"abc"
"aaa\"aaa"
"\x27"'''


def tokens(s):
    iterator = iter(s)
    for char in iterator:
        if char == "\\":
            char += next(iterator)
            if char.endswith("x"):
                char += next(iterator)
                char += next(iterator)
        yield char


def encoder(s):
    iterator = iter(s)
    yield '"'
    for char in iterator:
        if char == '"' or char == "\\":
            yield "\\"
        yield char
    yield '"'


def tokens_len(s):
    return sum(1 for token in tokens(s)) - 2


def length_diff(data):
    return sum(len(line) - tokens_len(line) for line in data.splitlines())


def encoded_diff(data):
    return sum(len("".join(encoder(line))) - len(line) for line in data.splitlines())


assert length_diff(test_data) == 12
assert encoded_diff(test_data) == 19

print(length_diff(data))
print(encoded_diff(data))
