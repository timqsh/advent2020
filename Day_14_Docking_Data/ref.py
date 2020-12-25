# type: ignore
import re
from pathlib import Path


def solve(txt: str, part: int) -> int:
    memory = {}
    lines = txt.splitlines()
    for line in lines:
        if m := re.match(r"^mask = ([10X]+)$", line):
            str_mask = m.group(1)
            mask0 = int(str_mask.replace("X", "1"), 2)
            mask1 = int(str_mask.replace("X", "0"), 2)
            maskX = int(str_mask.replace("1", "0").replace("X", "1"), 2)
        elif m := re.match(r"^mem\[(\d+)\] = (\d+)$", line):
            address, val = [int(g) for g in m.groups()]
            if part == 1:
                memory[address] = val | mask1 & mask0
            else:
                address = (address | mask1) & ~maskX
                sub_mask = maskX
                while True:
                    memory[address | sub_mask] = val
                    if sub_mask == 0:
                        break
                    sub_mask = (sub_mask - 1) & maskX
        else:
            raise ValueError(f"Unknown pattern {line}")
    return sum(memory.values())


test1 = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
assert 165 == solve(test1, 1)
test2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
assert 208 == solve(test2, 2)

text = (Path(__file__).parent / "input.txt").read_text()
print(solve(text, 1))
print(solve(text, 2))
