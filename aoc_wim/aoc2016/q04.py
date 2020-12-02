"""
--- Day 4: Security Through Obscurity ---
https://adventofcode.com/2016/day/4
"""
from collections import Counter
from collections import deque
from string import ascii_lowercase

from aocd import data
from parse import parse


def decrypt_name(encrypted_name, sector_id):
    d = deque(ascii_lowercase)
    d.rotate(-sector_id)
    lookup = {"-": " "}
    lookup.update(zip(ascii_lowercase, d))
    decrypted_name = "".join(lookup[k] for k in encrypted_name)
    return decrypted_name


sector_id_sum = 0
northpole_room = None
template = "{}-{:d}[{}]"
for line in data.splitlines():
    encrypted_name, sector_id, checksum = parse(template, line)
    counter = Counter(encrypted_name.replace("-", ""))
    most_common = sorted(counter, key=lambda k: (-counter[k], k))
    check = "".join(most_common[:5])
    if check == checksum:
        sector_id_sum += sector_id
    decrypted_name = decrypt_name(encrypted_name, sector_id)
    if "pole" in decrypted_name:
        northpole_room = sector_id


print("part a:", sector_id_sum)
print("part b:", northpole_room)
