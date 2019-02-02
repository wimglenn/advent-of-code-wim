import heapq
from collections import defaultdict
from itertools import count


class AStar:

    def __init__(self, state0, target):
        self.state0 = state0
        self.target = target
        self.closed = set()
        self.came_from = {}
        self.fscore = defaultdict(lambda: float("inf"), {target: self.heuristic(state0, target)})
        self.gscore = defaultdict(lambda: float("inf"), {state0: 0})

    def heuristic(self, state0, state1):
        """estimate of distance (cost) to get from state0 to state1
        note: in order for the heuristic to be admissible, this must
        not overestimate the actual distance (i.e. be optimistic)
        """
        return abs(state0 - state1)

    def cost(self, current_state, next_state):
        """actual delta to get from current state to an adjacent state"""
        return abs(current_state - next_state)

    def adjacent(self, state):
        """other states reachable from given state"""
        return []

    def reconstruct_path(self, current):
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
                return self.reconstruct_path(current_state)
            self.closed.add(current_state)
            for next_state in self.adjacent(current_state):
                if next_state in self.closed:
                    continue
                tentative_gscore = self.gscore[current_state] + self.cost(current_state, next_state)
                if tentative_gscore >= self.gscore[next_state]:
                    continue
                self.came_from[next_state] = current_state
                self.gscore[next_state] = tentative_gscore
                fscore = tentative_gscore + self.heuristic(next_state, self.target)
                self.fscore[next_state] = fscore
                heapq.heappush(heap, (fscore, next(i), next_state))
