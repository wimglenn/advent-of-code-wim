from aocd import data
import re


def req1(s):
    """
    Passwords must include one increasing straight of at least three letters, 
    like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd 
    doesn't count.
    """
    for a, b, c in zip(s, s[1:], s[2:]):
        ord_a = ord(a)
        if (0, ord(b)%ord_a, ord(c)%ord_a) == (0, 1, 2):
            return True
    else:
        return False


def req2(s):
    """
    Passwords may not contain the letters i, o, or l, as these letters can be 
    mistaken for other characters and are therefore confusing.
    """
    return 'i' not in s and 'o' not in s and 'l' not in s


def req3(s):
    """
    Passwords must contain at least two different, non-overlapping pairs of 
    letters, like aa, bb, or zz.
    """
    return len(re.findall(r'(.)\1', s)) >= 2


def is_valid(passwd):
    return req1(passwd) and req2(passwd) and req3(passwd)


def preprocess(s):
    result = ''
    for c in s:
        if c in 'iol':
            result += {'i': 'j', 'o': 'p', 'l': 'm'}[c]
            break
        else:
            result += c
    result += 'a'*(8-len(result))
    return result


def next_password(s):
    s = preprocess(s)
    alphabet = 'abcdefghjkmnpqrstuvwxyz'
    tr = dict(zip(alphabet, alphabet[1:]))
    while True:
        s_list = list(s)
        i = -1
        while True:
            try:
                s_list[i] = tr[s_list[i]]
            except KeyError:
                s_list[i] = 'a'
                i -= 1
            else:
                break
        s = ''.join(s_list)
        if is_valid(s):
            return s


assert req1('hijklmmn')
assert not req2('hijklmmn')
assert req3('abbceffg')
assert not req1('abbceffg')
assert not req3('abbcegjk')
assert next_password('abcdefgh') == 'abcdffaa'
assert next_password('ghijklmn') == 'ghjaabcc'


first = next_password(data)
print(first)
print(next_password(first))
