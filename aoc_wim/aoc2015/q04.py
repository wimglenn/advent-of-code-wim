import hashlib

from aocd import data


def mine(data, difficulty, start=0):
    secret_key = data.encode()
    prefix = "0" * difficulty
    h0 = hashlib.md5(secret_key).copy
    i = start
    while True:
        i += 1
        hash_ = h0()
        hash_.update(b"%d" % i)
        if hash_.hexdigest().startswith(prefix):
            return i


a = mine(data, difficulty=5)
print("part a:", a)
b = mine(data, difficulty=6, start=a - 1)
print("part b:", b)
