import itertools as it
import re
from typing import List, Tuple


def sum_values(txt: str) -> int:
    mem = {}
    lines = txt.splitlines()
    mask0 = 2 ** 36 - 1
    mask1 = 0
    for line in lines:
        if m := re.match(r"^mem\[(\d+)\] = (\d+)$", line):
            address, val = [int(g) for g in m.groups()]
            mem[address] = val | mask1 & mask0
        elif m := re.match(r"^mask = ([10X]+)$", line):
            ma = m.group(1)
            mask1 = int(ma.replace("X", "0"), 2)
            mask0 = int(ma.replace("X", "1"), 2)
        else:
            raise ValueError(f"Unknown pattern {line}")
    return sum(mem.values())


def part2(txt: str) -> int:
    mem = {}
    lines = txt.splitlines()
    masks: List[Tuple[int, int]] = []
    for line in lines:
        if m := re.match(r"^mem\[(\d+)\] = (\d+)$", line):
            address, val = [int(g) for g in m.groups()]
            for mask0, mask1 in masks:
                mem[(address | mask1) & mask0] = val
        elif m := re.match(r"^mask = ([10X]+)$", line):
            masks = []
            ma = m.group(1)
            x_pos = [m.start() for m in re.finditer("X", ma[::-1])]
            combinations = it.product([0, 1], repeat=len(x_pos))
            for comb in combinations:
                mask1 = int(ma.replace("X", "0"), 2)
                mask0 = 2 ** 36 - 1
                for i, c in enumerate(comb):
                    if c == 0:
                        mask0 &= ~(1 << x_pos[i])
                    else:
                        mask1 |= 1 << x_pos[i]
                masks.append((mask0, mask1))
        else:
            raise ValueError(f"Unknown pattern {line}")
    return sum(mem.values())


test1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
assert 165 == sum_values(test1)
test2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
assert 208 == part2(test2)

text = open("d14/input.txt").read()
print(sum_values(text))
print(part2(text))
