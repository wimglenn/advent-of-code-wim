from aocd import data


test_data = '10000'
test_len = 20


def dragon(a):
    return a + '0' + ''.join([{'0':'1', '1':'0'}[x] for x in a[::-1]])

def pad(s, n):
    return pad(dragon(s), n) if len(s) < n else s[:n]

def checksum(s):
    return ''.join(['01'[a==b] for a, b in zip(s[0::2], s[1::2])])

def r_checksum(s):
    s = checksum(s)
    return s if len(s)%2 else r_checksum(s)

def f(data, n):
    return r_checksum(pad(data.strip(), n))


assert f(test_data, test_len) == '01100'
print(f(data, 272))
print(f(data, 35651584))
