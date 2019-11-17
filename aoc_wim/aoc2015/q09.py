from itertools import permutations

from aocd import data


test_data = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""


def parsed(data):
    distances = {}
    cities = set()
    for line in data.splitlines():
        a, to, b, equals, n = line.split()
        cities |= {a, b}
        distances[(a, b)] = distances[(b, a)] = int(n)
    return cities, distances


def total_distance(route, distances):
    return sum(distances[p] for p in zip(route[:-1], route[1:]))


def get_routes(data):
    cities, distances = parsed(data)
    return {route: total_distance(route, distances) for route in permutations(cities)}


def get_shortest_route(data):
    routes = get_routes(data)
    return min(routes.values())


def get_longest_route(data):
    routes = get_routes(data)
    return max(routes.values())


assert get_shortest_route(test_data) == 605
print(get_shortest_route(data))

assert get_longest_route(test_data) == 982
print(get_longest_route(data))
