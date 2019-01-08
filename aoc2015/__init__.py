from collections import Counter


def ways(total, coins=(1,2,5,10,20,50,100)):
    ways = [[Counter()]] + [[] for _ in range(total)]
    for coin in coins:
        for i in range(coin, total + 1):
            ways[i] += [way + Counter({coin: 1}) for way in ways[i-coin]]
    return ways[total]
