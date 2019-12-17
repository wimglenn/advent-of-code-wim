from collections import Counter
from functools import lru_cache


def prod(vals, n=1):
    for val in vals:
        n *= val
    return n


def rsubset_sum(vals, target=0):
    # recursion impl

    @lru_cache(maxsize=None)
    def worker(hand=frozenset()):
        sum_ = sum(vals[i] for i in hand)
        if sum_ == target:
            result = {hand}
        elif sum_ > target:
            result = set()
        else:
            choices = set(range(len(vals))) - hand
            hands = (worker(hand | {choice}) for choice in choices)
            result = set.union(*hands)
        return result

    result = [[vals[i] for i in way] for way in set(worker())]
    return result


def subset_sum(vals, target=0):
    # dynamic programming impl
    sums = {0: [()]}  # key=sum, value=list of subsets for the sum
    if target in sums:
        yield from sums[target]  # annoying base case
    for val in vals:
        items = sums.items()  # don't change dict size during iteration
        sums = dict(items)
        for prev_sum, prev_subsets in items:
            sum_ = prev_sum + val
            subsets = [s + (val,) for s in prev_subsets]
            sums[sum_] = sums.get(sum_, []) + subsets
            if sum_ == target:
                yield from subsets


def ways(total, coins=(1, 2, 5, 10, 20, 50, 100)):
    ways = [[Counter()]] + [[] for _ in range(total)]
    for coin in coins:
        for i in range(coin, total + 1):
            ways[i] += [way + Counter({coin: 1}) for way in ways[i - coin]]
    return ways[total]


def dump_grid(g, clear=True):
    transform = {
        "#": "⬛",
        ".": "  ",
        "O": "🤖",
        "T": "🥇",
        ">": "➡️ ",
        "<": "⬅️ ",
        "^": "⬆️ ",
        "v": "⬇️ ",
    }
    empty = "  "
    print()
    xs = [int(z.real) for z in g]
    ys = [int(z.imag) for z in g]
    cols = range(min(xs), max(xs) + 1)
    rows = range(min(ys), max(ys) + 1)
    if clear:
        print("\033c")
    for row in rows:
        print(f"{row:>5d} ", end="")
        for col in cols:
            glyph = g.get(complex(col, row), empty)
            glyph = transform.get(glyph, glyph)
            print(glyph, end="")
        print()
    W = len(cols)
    footer_left = f"{cols[0]}".ljust(W * 2)
    footer_center = f"{cols[W//2]}".center(W * 2)
    footer_right = f"{cols[-1]}".rjust(W * 2)
    zf = zip(footer_left, footer_center, footer_right)
    footer = [next((x for x in iter([l, c, r]) if x != " "), " ") for (l, c, r) in zf]
    footer = "".join(footer)
    print(" " * 6 + footer)
    print()
