from aoc_wim.aoc2020 import q16

part_b_test_data = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


def test_identify_fields():
    fields, my_ticket, nearby_tickets = q16.parsed(part_b_test_data)
    valid_tickets = q16.get_valid_tickets(fields, nearby_tickets)
    known = q16.identify_fields(fields, valid_tickets)
    my_ticket_dict = q16.translate_my_ticket(known, my_ticket)
    assert my_ticket_dict == {
        "class": 12,
        "row": 11,
        "seat": 13,
    }
