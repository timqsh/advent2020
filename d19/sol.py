import re
from typing import Dict, List, NamedTuple


class Rule(NamedTuple):
    idx: int
    is_terminal: bool
    letters: str
    digits: List[List[int]]

    @staticmethod
    def from_string(s: str) -> "Rule":
        if m := re.match(r'^(\d+): "(\w)"$', s):
            return Rule(int(m.group(1)), True, m.group(2), [])
        elif m := re.match(r"^(\d+): ([\d \|]+)$", s):
            idx, groups = m.groups()
            digit_groups = groups.split("|")
            digits = [[int(d) for d in dg.split()] for dg in digit_groups]
            return Rule(int(idx), False, "", digits)
        raise ValueError(f"Can't parse rule {s}")


def create_re(rules_dict: Dict[int, Rule]) -> str:
    def helper(rule: Rule) -> str:
        if rule.is_terminal:
            return rule.letters
        else:
            result: List[str] = []
            for group in rule.digits:
                g = "".join([helper(rules_dict[dig]) for dig in group])
                result.append(g)
            return "(" + "|".join(result) + ")"

    zero = rules_dict[0]
    return "^" + helper(zero) + "$"


def solve_1(txt: str) -> int:
    rules_block, messages_block = txt.split("\n\n")
    rules = [Rule.from_string(s) for s in rules_block.splitlines()]
    rules_dict = {r.idx: r for r in rules}
    pattern = create_re(rules_dict)

    messages = messages_block.splitlines()
    total = 0
    for m in messages:
        if re.match(pattern, m):
            total += 1
    return total


test1 = """0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aba
aaa
bbb"""
test2 = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
assert solve_1(test2) == 2

test3 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31 | 42 42 31 31 | 42 42 42 31 31 31 | | 42 42 42 42 31 31 31 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


test3upd = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42 | 42 42 | 42 42 42 | 42 42 42 42 | 42 42 42 42 42 | 42 42 42 42 42 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""
assert solve_1(test3upd) == 12

text = open("d19/input.txt").read()
print(solve_1(text))

text = open("d19/input_upd.txt").read()
print(solve_1(text))
