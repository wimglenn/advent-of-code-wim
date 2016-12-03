import hashlib
from aocd import data


secret_key = data.strip()
i5 = i6 = None

i = 1
while True:
    text = u'{}{}'.format(secret_key, i)
    hash_ = hashlib.md5(text.encode('ascii')).hexdigest()
    if i5 is None and hash_.startswith('0'*5):
        i5 = i
    if i6 is None and hash_.startswith('0'*6):
        i6 = i
    i += 1
    if i5 is not None and i6 is not None:
        break

print(i5)
print(i6)
