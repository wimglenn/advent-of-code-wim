from aocd import data
from collections import Counter
import bisect
import logging


log = logging.getLogger(__name__)


tests = {
    """ 10 ORE => 10 A
        1 ORE => 1 B
        7 A, 1 B => 1 C
        7 A, 1 C => 1 D
        7 A, 1 D => 1 E
        7 A, 1 E => 1 FUEL""": (
        31,
        None,
    ),
    """ 9 ORE => 2 A
        8 ORE => 3 B
        7 ORE => 5 C
        3 A, 4 B => 1 AB
        5 B, 7 C => 1 BC
        4 C, 1 A => 1 CA
        2 AB, 3 BC, 4 CA => 1 FUEL""": (
        165,
        None,
    ),
    """ 157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""": (
        13312,
        82892753,
    ),
    """ 2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        17 NVRVD, 3 JNWZP => 8 VPVL
        53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        22 VJHF, 37 MNCFX => 5 FWMGM
        139 ORE => 4 NVRVD
        144 ORE => 7 JNWZP
        5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        145 ORE => 6 MNCFX
        1 NVRVD => 8 CXFTF
        1 VJHF, 6 MNCFX => 4 RFSQX
        176 ORE => 6 VJHF""": (
        180697,
        5586022,
    ),
    """ 171 ORE => 8 CNZTR
        7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
        114 ORE => 4 BHXH
        14 VRPVC => 6 BMBT
        6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
        6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
        15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
        13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
        5 BMBT => 4 WPTQ
        189 ORE => 9 KTJDG
        1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
        12 VRPVC, 27 CNZTR => 2 XDBXC
        15 KTJDG, 12 BHXH => 5 XCVML
        3 BHXH, 2 VRPVC => 7 MZWV
        121 ORE => 7 VRPVC
        7 XCVML => 6 RJRHP
        5 BHXH, 4 VRPVC => 5 LTCX""": (
        2210736,
        460664,
    ),
}


def parsed(data):
    trades = []
    for line in data.splitlines():
        sources, sep, dest = line.partition(" => ")
        src = Counter()
        for source in sources.split(", "):
            n, source = source.split()
            src[source] += int(n)
        n, dest = dest.split()
        dst = Counter({dest: int(n)})
        trades.append((dst, src))
    assert len(trades) == len({k for src, dst in trades for k in dst})
    return trades


def make_only_trade(have, trades):
    for elem, need in have.items():
        if not any(elem in dst for src, dst in trades):
            src, dst = next((src, dst) for (src, dst) in trades if list(src) == [elem])
            if src[elem] >= need:
                log.debug("trading (only) %s -> %s", src, dst)
                have -= src
                have += dst
                trades.remove((src, dst))
                return src, dst


def make_unique_trade(have, trades):
    for elem, avail in have.items():
        options = [(src, dst) for (src, dst) in trades if list(src) == [elem]]
        if len(options) == 1:
            [(src, dst)] = options
            if have[elem] >= src[elem]:
                r = have[elem] // src[elem] - 1
                factor = r or 1
                log.debug("trading (unique) x%d %s -> %s", factor, src, dst)
                have -= Counter({k: v * factor for k, v in src.items()})
                have += Counter({k: v * factor for k, v in dst.items()})
                return src, dst


def get_only_trade(have, trades):
    options = {}
    for elem, avail in have.items():
        if elem == "ORE":
            continue
        elem_options = [(src, dst) for (src, dst) in trades if list(src) == [elem]]
        if elem_options:
            options[elem] = elem_options
    if len(options) == 1:
        [(elem, trades)] = options.items()
        if len(trades) == 1:
            [(src, dst)] = trades
            return src, dst


def get_any_trade(have, trades):
    for elem, avail in have.items():
        if elem == "ORE":
            continue
        for src, dst in trades:
            if elem in src:
                return src, dst


def part_a(data, fuel=1):
    trades = parsed(data)
    have = Counter({"FUEL": fuel})
    while list(have) != ["ORE"]:
        if make_only_trade(have, trades):
            continue
        if make_unique_trade(have, trades):
            continue
        raise Exception("stuck")
    result = have["ORE"]
    return result


def part_b(data):
    n_ore = 1000000000000
    lo = fuel = 1
    n = part_a(data, fuel=lo)
    assert n < n_ore
    while True:
        fuel *= 2
        n = part_a(data, fuel)
        if n < n_ore:
            lo = fuel
        else:
            hi = fuel
            break

    assert lo < hi
    assert part_a(data, lo) < n_ore
    assert part_a(data, hi) >= n_ore

    class Wrapper:
        def __getitem__(self, item):
            return part_a(data, fuel=item) >= n_ore

    search = Wrapper()
    pos = bisect.bisect_right(search, 0.5, lo, hi)
    assert part_a(data, fuel=pos - 1) < n_ore
    assert part_a(data, fuel=pos) >= n_ore
    return pos - 1


for test_data, (a, b) in tests.items():
    assert part_a(test_data) == a
    assert b is None or part_b(test_data) == b


print(part_a(data))
print(part_b(data))
