from math import prod
from pathlib import Path
from typing import List, Tuple


def parse(txt: str) -> Tuple[int, List[int], List[int]]:
    line1, line2 = txt.splitlines()
    idx, busses = parse_line(line2)
    return int(line1), list(idx), list(busses)


def parse_line(line: str) -> Tuple[List[int], List[int]]:
    idx, busses = zip(*[(i, int(c)) for i, c in enumerate(line.split(",")) if c != "x"])
    return list(idx), list(busses)


def part1(txt: str) -> int:
    current_timestamp, _, busses = parse(txt)
    elem = min(busses, key=lambda x: x - (current_timestamp % x))
    minutes_to_wait = elem - (current_timestamp % elem)
    return elem * minutes_to_wait


def part2(line: str) -> int:
    a, n = parse_line(line)
    for i in range(len(a)):
        a[i] = n[i] - a[i]
    return chinese_remainder(n, a)


def chinese_remainder(n: List[int], a: List[int]) -> int:
    sum = 0
    product = prod(n)
    for n_i, a_i in zip(n, a):
        p = product // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % product


def mul_inv(a: int, b: int) -> int:
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


test1 = """939
7,13,x,x,59,x,31,19"""
assert part1(test1) == 295


assert part2("17,x,13,19") == 3417.0
assert part2("67,7,59,61") == 754018.0
assert part2("67,x,7,59,61") == 779210.0
assert part2("67,7,x,59,61") == 1261476.0
assert part2("1789,37,47,1889") == 1202161486

text = (Path(__file__).parent / "input.txt").read_text()
res1 = part1(text)
print(res1)
assert res1 == 3385
res2 = part2(text.splitlines()[1])
print(res2)
assert res2 == 600689120448303
