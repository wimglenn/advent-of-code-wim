"""
--- Day 19: Not Enough Minerals ---
https://adventofcode.com/2022/day/19
"""
from aocd import data
from parse import parse
from typing import NamedTuple


template = (
    "Blueprint {id:d}: "
    "Each ore robot costs {ore_ore:d} ore. "
    "Each clay robot costs {cla_ore:d} ore. "
    "Each obsidian robot costs {obs_ore:d} ore and {obs_cla:d} clay. "
    "Each geode robot costs {geo_ore:d} ore and {geo_obs:d} obsidian."
)
if len(data.split("\n\n")) == 2:
    lines = data.replace("  ", " ").replace("\n\n", " --- ").replace("\n", "").split(" --- ")
else:
    lines = data.splitlines()


class Node(NamedTuple):
    n_geo: int = 0
    n_obs: int = 0
    n_cla: int = 0
    n_ore: int = 0

    r_geo: int = 0
    r_obs: int = 0
    r_cla: int = 0
    r_ore: int = 1

    def buy(self, rtype=None):
        n_geo = self.n_geo + self.r_geo
        n_obs = self.n_obs + self.r_obs
        n_cla = self.n_cla + self.r_cla
        n_ore = self.n_ore + self.r_ore
        r_geo = self.r_geo
        r_obs = self.r_obs
        r_cla = self.r_cla
        r_ore = self.r_ore
        if rtype == "geo":
            r_geo += 1
        elif rtype == "obs":
            r_obs += 1
        elif rtype == "cla":
            r_cla += 1
        elif rtype == "ore":
            r_ore += 1
        if rtype is not None:
            cost_obs, cost_cla, cost_ore = bp[f"cost_{rtype}"]
            n_obs -= cost_obs
            n_cla -= cost_cla
            n_ore -= cost_ore
        return Node(n_geo, n_obs, n_cla, n_ore, r_geo, r_obs, r_cla, r_ore)


blueprints = []
rtypes = "ore", "cla", "obs", "geo"
for line in lines:
    parsed = parse(template, line).named
    bp = {"pk": parsed["id"]}
    costs = []
    for r0 in rtypes:
        k = f"cost_{r0}"
        cost = parsed.get(f"{r0}_obs", 0), parsed.get(f"{r0}_cla", 0), parsed.get(f"{r0}_ore", 0)
        bp[k] = cost
        costs.append(cost)
    bp["max_ore"] = max(c[2] for c in costs)
    bp["max_cla"] = max(c[1] for c in costs)
    bp["max_obs"] = max(c[0] for c in costs)
    blueprints.append(bp)


def adj(n0):
    result = []
    c_obs, c_cla, c_ore = bp["cost_geo"]
    if c_obs <= n0.n_obs and c_ore <= n0.n_ore:
        result.append(n0.buy(rtype="geo"))

    c_obs, c_cla, c_ore = bp["cost_obs"]
    if c_cla <= n0.n_cla and c_ore <= n0.n_ore and n0.r_geo <= 2 and n0.r_obs < bp["max_obs"]:
        result.append(n0.buy(rtype="obs"))

    c_obs, c_cla, c_ore = bp["cost_cla"]
    if c_ore <= n0.n_ore and n0.r_obs <= 2 and n0.r_geo == 0 and n0.r_cla < bp["max_cla"]:
        result.append(n0.buy(rtype="cla"))

    c_obs, c_cla, c_ore = bp["cost_ore"]
    if c_ore <= n0.n_ore and n0.r_cla <= 2 and n0.r_obs == 0 and n0.r_geo == 0 and n0.r_ore < bp["max_ore"]:
        result.append(n0.buy(rtype="ore"))

    result.append(n0.buy())  # buy nothing - increases budget and elapsed time
    return result


class DFS:

    def __init__(self, adj, max_depth=None):
        self.adj = adj
        self.seen = {}
        self.max_depth = max_depth

    def __call__(self, s0, target=None):
        stack = [(0, s0)]
        maxd = self.max_depth or float("inf")
        seen = self.seen
        best = 0
        while stack:
            depth, state = stack.pop()
            if state in seen and seen[state] <= depth:
                # already got here by a more efficient path - don't bother extending
                continue
            seen[state] = depth
            if state.n_geo > best:
                best = state.n_geo
                print(f"new best {best} - {len(seen)} {len(stack)} depth={depth}, {state}")
            if depth + 1 <= maxd:
                t_remain = maxd - depth
                potential = state.n_geo + t_remain * state.r_geo + (t_remain * (t_remain - 1))//2
                if potential >= best:
                    stack += [(depth + 1, s) for s in self.adj(state)[::-1]]
        return best


a = 0
for bp in blueprints:
    bfs = DFS(adj, max_depth=24)
    bfs(Node())
    best = max([s.n_geo for s, d in bfs.seen.items() if d == 24])
    print(f"n_geodes={best} blueprint={bp}")
    a += bp["pk"] * best
print("part a:", a)

b = 1
for bp in blueprints[:3]:
    bfs = DFS(adj, max_depth=32)
    bfs(Node())
    best = max([s.n_geo for s, d in bfs.seen.items() if d == 32])
    print(f"n_geodes={best} blueprint={bp}")
    b *= best
print("part b:", b)
