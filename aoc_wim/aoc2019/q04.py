from aocd import data


def ok(n, part="a"):
    # It is a six-digit number.
    if not (100_000 <= n <= 999_999):
        return False

    # Two adjacent digits are the same. (part a)
    # ... but not part of a larger group of matching digits (part b)
    str_n = str(n)
    for s in "0123456789":
        if 2 * s in str_n:
            if part == "a":
                break
            elif part == "b" and 3 * s not in str_n:
                break
    else:
        return False

    # Going from left to right, the digits never decrease
    for i in range(5):
        if str_n[i + 1] < str_n[i]:
            return False

    return True


def count(data, part="a"):
    lo, hi = [int(x) for x in data.split("-")]
    result = sum(1 for n in range(lo, hi + 1) if ok(n, part=part))
    return result


assert ok(111111, part="a")
assert not ok(223450, part="a")
assert not ok(123789, part="a")

assert ok(112233, part="b")
assert not ok(123444, part="b")
assert ok(111122, part="b")

print(count(data, part="a"))
print(count(data, part="b"))
