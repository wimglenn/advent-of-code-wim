"""
--- Day 4: Passport Processing ---
https://adventofcode.com/2020/day/4
"""
from aocd import data
from marshmallow import INCLUDE
from marshmallow import Schema
from marshmallow.fields import Integer
from marshmallow.fields import String
from marshmallow.validate import OneOf
from marshmallow.validate import Range
from marshmallow.validate import Regexp
from marshmallow.validate import Validator
from marshmallow.validate import ValidationError


class Height(Validator):
    def __call__(self, value):
        if value.endswith("cm"):
            Range(min=150, max=193)(int(value[:-2]))
        elif value.endswith("in"):
            Range(min=59, max=76)(int(value[:-2]))
        else:
            raise ValidationError("height must be cm or in")
        return value


class PassportSchema(Schema):
    byr = Integer(validate=Range(min=1920, max=2002))
    iyr = Integer(validate=Range(min=2010, max=2020))
    eyr = Integer(validate=Range(min=2020, max=2030))
    hgt = String(validate=Height())
    hcl = String(validate=Regexp(r"^#[0-9a-f]{6}$"))
    ecl = String(validate=OneOf("amb blu brn gry grn hzl oth".split()))
    pid = String(validate=Regexp(r"^[0-9]{9}$"))

    class Meta:
        unknown = INCLUDE


schema = PassportSchema()
a = b = 0
for block in data.split("\n\n"):
    passport_data = dict(x.split(":") for x in block.split())
    if not (passport_data.keys() >= schema.fields.keys()):
        continue
    a += 1
    errors = schema.validate(passport_data)
    b += not errors

print("part a:", a)
print("part b:", b)
