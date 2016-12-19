from aocd import data
from itertools import cycle
from collections import deque, OrderedDict
import numpy as np
import sys


'''
elves = np.array(list(enumerate([1]*n, 1)), dtype=int)

while len(elves) > 1:
    busted_elves = elves[1::2]
    busted_elves[:,0] = 0
    elves[0::2][:len(busted_elves)] += busted_elves
    roll = len(elves)%2
    elves = elves[elves[:,0].astype(bool)]
    if roll:
        elves = np.roll(elves, 1, axis=0)

assert elves[0][1] == n
print(elves)[0][0]  # part a: 1842613 
'''

n = int(data)
n = 33

elves = [(i, 1) for i in range(1, n+1)]

k = 0
i = 0
while len(elves) > 1:
    victim = i + len(elves)//2
    victim %= len(elves)
    print(elves[i][0], elves[victim][0])
    elves[i] = elves[i][0], elves[i][1] + elves[victim][1]
    elves.pop(victim)
    if victim >= i:
        i += 1
    if i == len(elves):
        i = 0
        # print(elves)

print elves

