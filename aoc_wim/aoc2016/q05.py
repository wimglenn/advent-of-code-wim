"""
--- Day 5: How About a Nice Game of Chess? ---
https://adventofcode.com/2016/day/5
"""
from aocd import data
import os
from collections import deque
from concurrent.futures import ProcessPoolExecutor
from aoc_wim.aoc2016 import md5_miner_q05
from itertools import count


def main():
    code1 = []
    code2 = ["."] * 8
    remaining = set("01234567")
    chunksize = 50000
    blocks = ((data, i0, chunksize) for i0 in count(step=chunksize))
    with ProcessPoolExecutor() as pool:
        futures = deque([pool.submit(md5_miner_q05, *next(blocks)) for _ in range(os.cpu_count())])
        while True:
            for n, md5sum in futures.popleft().result():
                h5, h6 = md5sum[5], md5sum[6]
                code1.append(h5)
                if h5 in remaining:
                    code2[int(h5)] = h6
                    remaining.remove(h5)
            if not remaining:
                break
            futures.append(pool.submit(md5_miner_q05, *next(blocks)))

    print("part a:", "".join(code1[:8]))
    print("part b:", "".join(code2))


if __name__ == "__main__":
    main()
