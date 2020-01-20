import hashlib

from aocd import data


def mine(data, difficulty, start=0):
    secret_key = data.encode()
    prefix = "0" * difficulty
    i = start
    while True:
        i += 1
        hash_ = hashlib.md5(b"%s%d" % (secret_key, i)).hexdigest()
        if hash_.startswith(prefix):
            return i


a = mine(data, difficulty=5)
print("part a:", a)
b = mine(data, difficulty=6, start=a - 1)
print("part b:", b)
