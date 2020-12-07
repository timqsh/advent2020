import functools
import re
from typing import Dict

TEXT = open("d7/input.txt").read()
TEST1 = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
TEST2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
MY_BAG = "shiny gold"

Rules = Dict[str, Dict[str, int]]


def parse_text(txt: str) -> Rules:
    lines = txt.splitlines()
    rules = {}
    for line in lines:
        if not (m := re.match(r"(.*) bags contain (.*)", line)):
            raise ValueError(f"can't parse {line}")
        target, contents_str = m.groups()
        contents = re.findall(r"(\d+) (\w+ \w+)", contents_str)
        rules[target] = dict((color, int(num)) for num, color in contents)
    return rules


def count_bags_which_contain(bag: str, rules: Rules) -> int:
    @functools.lru_cache(None)
    def dfs(out_bag: str) -> bool:
        return out_bag == bag or any(dfs(content) for content in rules[out_bag])

    return sum(dfs(out_bag) for out_bag in rules.keys()) - 1


def count_bags_inside(bag: str, rules: Rules) -> int:
    @functools.lru_cache(None)
    def dfs(bag: str) -> int:
        return 1 + sum([num * dfs(b) for b, num in rules[bag].items()])

    return dfs(bag) - 1


rules1 = parse_text(TEST1)
rules2 = parse_text(TEST2)
assert count_bags_which_contain(MY_BAG, rules1) == 4
assert count_bags_inside(MY_BAG, rules1) == 32
assert count_bags_inside(MY_BAG, rules2) == 126

my_rules = parse_text(TEXT)
print(f"`{MY_BAG}` is in {count_bags_which_contain(MY_BAG, my_rules)} other bags")
print(f"`{MY_BAG}` contains {count_bags_inside(MY_BAG, my_rules)} other bags")
