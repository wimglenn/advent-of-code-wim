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


def part_ab(data):
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
    return sector_id_sum, northpole_room


test_data = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""


assert part_ab(test_data)[0] == 1514
assert decrypt_name("qzmt-zixmtkozy-ivhz", 343) == "very encrypted name"


a, b = part_ab(data)
print("part a:", a)
print("part b:", b)
