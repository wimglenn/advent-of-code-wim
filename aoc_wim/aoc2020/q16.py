"""
--- Day 16: Ticket Translation ---
https://adventofcode.com/2020/day/16
"""
from aocd import data
from math import prod


def parsed(data):
    fields_raw, my_ticket_raw, nearby_tickets_raw = data.split("\n\n")

    fields = {}
    for field in fields_raw.splitlines():
        name, ranges = field.split(": ")
        fields[name] = []
        for r in ranges.split(" or "):
            start, stop = r.split("-")
            fields[name].append(range(int(start), int(stop) + 1))

    _, my_ticket = my_ticket_raw.splitlines()
    my_ticket = [int(x) for x in my_ticket.split(",")]
    
    _, *nearby_tickets = nearby_tickets_raw.splitlines()
    nearby_tickets = [[int(x) for x in row.split(",")] for row in nearby_tickets]

    return fields, my_ticket, nearby_tickets


def identify_fields(fields, valid_tickets):
    cols = [*zip(*valid_tickets)]  # zip-splat transpose trick
    known = {}
    while len(known) < len(fields):
        for i, col in enumerate(cols):
            possibilities = []
            for name, (r1, r2) in fields.items():
                if name not in known and all(v in r1 or v in r2 for v in col):
                    possibilities.append(name)
            if len(possibilities) == 1:
                [name] = possibilities
                known[name] = i
    return known


def get_valid_tickets(fields, nearby_tickets):
    invalid = set()
    a = 0
    for i, ns in enumerate(nearby_tickets):
        for n in ns:
            for _, ranges in fields.items():
                if any(n in r for r in ranges):
                    break  # valid
            else:
                invalid.add(i)
                a += n
    print("part a:", a)
    valid_tickets = [nn for i, nn in enumerate(nearby_tickets) if i not in invalid]
    return valid_tickets


def translate_my_ticket(fieldname2col, my_ticket):
    return {name: my_ticket[col] for name, col in fieldname2col.items()}


if __name__ == "__main__":
    fields, my_ticket, nearby_tickets = parsed(data)
    valid_tickets = get_valid_tickets(fields, nearby_tickets)
    known = identify_fields(fields, valid_tickets)
    my_ticket_dict = translate_my_ticket(known, my_ticket)
    b = prod(v for k, v in my_ticket_dict.items() if k.startswith("departure"))
    print("part b:", b)
