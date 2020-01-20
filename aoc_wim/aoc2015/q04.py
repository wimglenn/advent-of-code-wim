import hashlib

from aocd import data


def mine(data, difficulty):
    secret_key = data.encode()
    prefix = "0" * difficulty
    i = 0
    while True:
        i += 1
        hash_ = hashlib.md5(b"%s%d" % (secret_key, i)).hexdigest()
        if hash_.startswith(prefix):
            return i


print("part a:", mine(data, difficulty=5))
print("part b:", mine(data, difficulty=6))
