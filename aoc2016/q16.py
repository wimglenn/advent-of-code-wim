from aocd import data


test_data = '10000'
test_len = 20


def dragon(a):
    b = a[::-1]
    tr = {'0': '1', '1': '0'}
    b = ''.join([tr[x] for x in b])
    result = a + '0' + b
    return result

def pad(s, target_len):
    while len(s) < target_len:
        s = dragon(s)
    return s[:target_len]

def checksum(s):
    return ''.join(['01'[a==b] for a, b in zip(s[0::2], s[1::2])])

def n_checksum(s):
    s = checksum(s)
    while len(s) % 2 == 0:
        s = checksum(s)
    return s

def f(data, len_):
    return n_checksum(pad(data.strip(), len_))


assert f(test_data, test_len) == '01100'
print(f(data, 272))  # part A: 11100111011101111
print(f(data, 35651584))  # part B: 10001110010000110
