"""
--- Day 25: Combo Breaker ---
https://adventofcode.com/2020/day/25
"""
from aocd import data


def crack(pk_card, pk_door, subject_number=7, modulus=20201227):
    loop_size = 0
    p = 1
    while True:
        loop_size += 1
        p = p * subject_number % modulus
        if p == pk_card:
            return pow(pk_door, loop_size, modulus)
        if p == pk_door:
            return pow(pk_card, loop_size, modulus)


pk_card, pk_door = data.split()
print(crack(int(pk_card), int(pk_door)))
