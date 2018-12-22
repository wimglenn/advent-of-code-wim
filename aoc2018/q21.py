part_a = part_b = None
seen = set()
r3 = 0x10000
r5 = 733884
while True:
    r5 += r3 & 0xff
    r5 &= 0xffffff
    r5 *= 65899
    r5 &= 0xffffff
    if r3 >= 256:
        r3 //= 256
        continue
    if part_a is None:
        part_a = r5
    if r5 in seen:
        break
    part_b = r5
    seen.add(r5)
    r3 = r5 | 0x10000
    r5 = 733884

print(part_a)  # 2884703
print(part_b)  # 15400966
