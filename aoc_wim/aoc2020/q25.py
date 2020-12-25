"""
--- Day 25: Combo Breaker ---
https://adventofcode.com/2020/day/25
"""
from aocd import data

pk_card, pk_door = [int(line) for line in data.split()]
subject_number = 7
modulus = 20201227

loop_size = 0
while True:
    loop_size += 1
    p = pow(subject_number, loop_size, modulus)
    if p == pk_card:
        print(pow(pk_door, loop_size, modulus))
        break
    if p == pk_door:
        print(pow(pk_card, loop_size, modulus))
        break
