import hashlib

from aocd import data


def mine(data, difficulty):
    secret_key = data.strip()
    i = 1
    while True:
        text = u"{}{}".format(secret_key, i)
        hash_ = hashlib.md5(text.encode("ascii")).hexdigest()
        if hash_.startswith("0" * difficulty):
            return i
        i += 1


a_tests = {
    "abcdef": 609043,
    "pqrstuv": 1048970,
}
for test_data, expected in a_tests.items():
    assert mine(test_data, difficulty=5) == expected


print("part a:", mine(data, difficulty=5))
print("part b:", mine(data, difficulty=6))
