"""
--- Day 14: One-Time Pad ---
https://adventofcode.com/2016/day/14
"""
import os
import re
from collections import defaultdict
from collections import deque
from aocd import data
from aoc_wim.aoc2016 import md5_miner_q14a
from aoc_wim.aoc2016 import md5_miner_q14b
from concurrent.futures import ProcessPoolExecutor
from itertools import count


def search(data, stretch):
    keys = []
    triples = defaultdict(list)
    pat3 = re.compile(r"(.)\1{2}")
    pat5 = re.compile(r"(.)\1{4}")
    i = 0
    stop = None
    miner = md5_miner_q14b if stretch else md5_miner_q14a
    chunksize = 50 if stretch else 50000
    blocks = ((data, i0, chunksize) for i0 in count(step=chunksize))
    with ProcessPoolExecutor() as pool:
        futures = deque([pool.submit(miner, *next(blocks)) for _ in range(os.cpu_count())])
        while True:
            for i, md5sum in futures.popleft().result():
                triple = pat3.search(md5sum)
                for quintuple in pat5.findall(md5sum):
                    keys.extend([x for x in triples[quintuple] if i - x <= 1000])
                    triples[quintuple].clear()  # avoid to count same key twice
                    if stop is None and len(keys) >= 64:
                        stop = i + 1001
                triples[triple.group()[0]].append(i)
            if stop is not None and i > stop:
                break
            futures.append(pool.submit(miner, *next(blocks)))
        return sorted(keys)[63]


if __name__ == "__main__":
    print("part a:", search(data, stretch=False))
    print("part b:", search(data, stretch=True))
