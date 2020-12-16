import re
from typing import List, NamedTuple, Tuple


class Rule(NamedTuple):
    name: str
    lo1: int
    hi1: int
    lo2: int
    hi2: int

    @staticmethod
    def from_string(s: str) -> "Rule":
        if m := re.match(r"^([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)", s):
            return Rule(m.group(1), *map(int, m.groups()[1:]))
        raise ValueError(f"Can't parse as rule: {s}")

    def match(self, field: int) -> bool:
        return self.lo1 <= field <= self.hi1 or self.lo2 <= field <= self.hi2


Tickets = List[List[int]]


def parse_input(txt: str) -> Tuple[List[Rule], List[int], Tickets]:
    rules_block, my_block, tickets_block = txt.split("\n\n")
    rules = [Rule.from_string(r) for r in rules_block.splitlines()]
    my = [int(f) for f in my_block.splitlines()[1].split(",")]
    tickets = [[int(f) for f in t.split(",")] for t in tickets_block.splitlines()[1:]]
    return rules, my, tickets


def invalid_fields(rules: List[Rule], ticket: List[int]) -> List[int]:
    return [f for f in ticket if not any(r.match(f) for r in rules)]


def part1(rules: List[Rule], tickets: Tickets) -> int:
    return sum(sum(invalid_fields(rules, t)) for t in tickets)


def valid_tickets(rules: List[Rule], tickets: Tickets) -> Tickets:
    return [t for t in tickets if not invalid_fields(rules, t)]


def deduce_names(rules: List[Rule], tickets: Tickets) -> List[str]:
    all_possible: List[List[Rule]] = []
    for col in zip(*tickets):
        possible = [r for r in rules if all(r.match(field) for field in col)]
        all_possible.append(possible)
    result = [""] * len(rules)
    for i, possible in sorted(enumerate(all_possible), key=lambda x: len(x[1])):
        uniq = [r for r in possible if r.name not in result]
        result[i] = uniq[0].name
    return result


if __name__ == "__main__":
    test1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    rules, my, tickets = parse_input(test1)
    assert part1(rules, tickets) == 71
    assert valid_tickets(rules, tickets) == [[7, 3, 47]]

    test2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
    rules, my, tickets = parse_input(test2)
    names = deduce_names(rules, tickets)
    assert names == ["row", "class", "seat"]

    txt = open("d16/input.txt").read()
    rules, my, tickets = parse_input(txt)
    result = part1(rules, tickets)
    print(result)
    assert result == 29019

    valid = valid_tickets(rules, tickets)
    names = deduce_names(rules, valid)
    result = 1
    for name, field in zip(names, my):
        if name.startswith("departure"):
            result *= field
    print(result)
    assert result == 517827547723
