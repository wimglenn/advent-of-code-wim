import heapq
from collections import defaultdict
from itertools import count
import logging


log = logging.getLogger(__name__)


class AStar:
    def __init__(self, state0, target):
        self.state0 = state0
        self.target = target
        self.closed = set()
        self.came_from = {}
        inf = float("inf")
        # optimistic estimate of cost to reach node
        self.fscore = defaultdict(lambda: inf, {target: self.heuristic(state0, target)})
        # shortest cost to reach node found so far
        self.gscore = defaultdict(lambda: inf, {state0: 0})
        self.path_length = None

    def heuristic(self, state0, state1):
        """estimate of distance (cost) to get from state0 to state1
        note: in order for the heuristic to be admissible, this must
        not overestimate the actual distance (i.e. be optimistic)
        """
        return 1

    def cost(self, current_state, next_state):
        """actual delta to get from current state to an adjacent state"""
        return 1

    def adjacent(self, state):
        """other states reachable from given state"""
        return []

    def reconstruct_path(self, current=None):
        if current is None:
            current = self.target
        path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        return path

    def target_reached(self, current_state, target):
        return current_state == target

    def run(self):
        i = count()  # tie-breaker
        heap = [(0, next(i), self.state0)]
        while heap:
            _score, _id, current_state = heapq.heappop(heap)
            if self.target_reached(current_state, self.target):
                path_to_target = self.reconstruct_path(current_state)
                self.path_length = len(path_to_target) - 1
                if self.target is None:
                    self.target = current_state
                return path_to_target
            self.closed.add(current_state)
            for next_state in self.adjacent(current_state):
                if next_state in self.closed:
                    continue
                tentative_gscore = self.gscore[current_state]
                tentative_gscore += self.cost(current_state, next_state)
                if tentative_gscore >= self.gscore[next_state]:
                    continue
                self.came_from[next_state] = current_state
                self.gscore[next_state] = tentative_gscore
                fscore = tentative_gscore + self.heuristic(next_state, self.target)
                self.fscore[next_state] = fscore
                heapq.heappush(heap, (fscore, next(i), next_state))


class BisectError(Exception):
    pass


class Bisect:

    def __init__(self, callable, val=0.5, lo=None, hi=None):
        self.callable = callable
        self.val = val
        self.lo = lo
        self.hi = hi
        self.results = {}

    def discover_bounds(self):
        step = 1
        if self.lo is None:
            pos = 0
            if self.hi is not None:
                pos = self.hi - 1
            while True:
                self.results[pos] = result = self.callable(pos)
                log.debug("discovering lower bound %s: %s", pos, result)
                if result < self.val:
                    self.lo = pos
                    break
                if self.hi is not None:
                    self.hi = min(self.hi, pos)
                pos -= step
                step *= 2
        step = 1
        if self.hi is None:
            pos = self.lo + 1
            while True:
                self.results[pos] = result = self.callable(pos)
                log.debug("discovering upper bound %s: %s", pos, result)
                if self.val <= result:
                    self.hi = pos
                    break
                self.lo = max(self.lo, pos)
                pos += step
                step *= 2
        if self.lo > self.hi:
            raise BisectError("error discovering bounds")
        if self.results[self.lo] > self.results[self.hi]:
            raise BisectError("callable isn't non-decreasing between %s and %s", self.lo. self.hi)

    def step(self):
        mid = (self.lo + self.hi) // 2
        self.results[mid] = result = self.callable(mid)
        log.debug("bisected %s: %s", mid, result)
        if result < self.val:
            self.lo = mid
        elif self.val <= result:
            self.hi = mid

    def run(self):
        if self.lo is None or self.hi is None:
            self.discover_bounds()
        while self.hi - self.lo > 1:
            self.step()
        return self.lo
