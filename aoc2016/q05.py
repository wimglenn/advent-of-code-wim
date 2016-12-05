from aocd import data
from hashlib import md5


data = data.strip()

code1 = ''
code2 = [None] * 8
n = 0
while True:
    test = '{}{}'.format(data, n).encode('ascii')
    hash_ = md5(test).hexdigest()
    if hash_.startswith('0'*5):
        code1 += hash_[5]
        if hash_[5] in '01234567':
            pos = int(hash_[5])
        if code2[pos] is None:
            code2[pos] = hash_[6]
    if None not in code2 and len(code1) > 7:
        break
    n += 1

code1 = code1[:8]
code2 = ''.join(code2)

print(code1)
print(code2)
