from aocd import data
from collections import Counter, deque
from string import ascii_lowercase


sector_id_sum = 0
northpole_rooms = []

for line in data.splitlines():
    encrypted_name, sector_id_and_checksum = line.rsplit('-', 1)
    sector_id, checksum = sector_id_and_checksum[:-1].split('[')
    sector_id = int(sector_id)
    counter = Counter(encrypted_name.replace('-', ''))
    most_common = sorted(counter, key=lambda k: (-counter[k], k))
    check = ''.join(most_common[:5])
    if check == checksum:
        sector_id_sum += sector_id
    deque_ = deque(ascii_lowercase)
    deque_.rotate(-sector_id)
    lookup = {'-': ' '}
    lookup.update(zip(ascii_lowercase, deque_))
    decrypted_name = ''.join(lookup[k] for k in encrypted_name)
    if 'pole' in decrypted_name:
        northpole_rooms.append(sector_id)

[northpole_room] = northpole_rooms

print(sector_id_sum)
print(northpole_room)
