import json
import re

from aocd import data


def sum_of_numbers_in_text(s):
    return sum(int(n) for n in re.findall(r"-?\d+", s))


def rsum(data):
    if isinstance(data, int):
        return data
    elif isinstance(data, dict):
        if "red" in data.values():
            return 0
        return rsum(list(data.values()))
    elif isinstance(data, list):
        return sum(rsum(n) for n in data)
    else:
        return 0


assert sum_of_numbers_in_text("[1,2,3]") == 6
assert sum_of_numbers_in_text('{"a":2,"b":4}') == 6
assert sum_of_numbers_in_text("[[[3]]]") == 3
assert sum_of_numbers_in_text('{"a":{"b":4},"c":-1}') == 3
assert sum_of_numbers_in_text('{"a":[-1,1]}') == 0
assert sum_of_numbers_in_text('[-1,{"a":1}]') == 0
assert sum_of_numbers_in_text("[]") == 0
assert sum_of_numbers_in_text("{}") == 0

assert rsum([1, 2, 3]) == 6
assert rsum([1, {"c": "red", "b": 2}, 3]) == 4
assert rsum({"d": "red", "e": [1, 2, 3, 4], "f": 5}) == 0
assert rsum([1, "red", 5]) == 6


print(sum_of_numbers_in_text(data))
print(rsum(json.loads(data)))
