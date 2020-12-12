from dataclasses import dataclass
from typing import List, Tuple

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIR_NAMES = dict(zip("ESWN", DIRS))

Instructions = List[Tuple[str, int]]


def parse(txt: str) -> Instructions:
    return [(l[0], int(l[1:])) for l in txt.splitlines()]


@dataclass
class Ship1:
    x: int = 0
    y: int = 0
    dir_idx: int = 0

    def move(self, s: str, num: int) -> None:
        if s in DIR_NAMES:
            dx, dy = DIR_NAMES[s]
            self.x += dx * num
            self.y += dy * num
        elif s == "F":
            dx, dy = DIRS[self.dir_idx]
            self.x += dx * num
            self.y += dy * num
        elif s in "LR":
            count = num // 90
            if s == "L":
                count = 4 - count
            self.dir_idx = (self.dir_idx + count) % 4

    def run(self, instructions: Instructions) -> None:
        for s, num in instructions:
            self.move(s, num)

    @classmethod
    def solve(cls, txt: str) -> int:
        instructions = parse(txt)
        obj = cls()
        obj.run(instructions)
        return obj.manhatten()

    def manhatten(self) -> int:
        return abs(self.x) + abs(self.y)


@dataclass
class Ship2(Ship1):
    wpx: int = 10
    wpy: int = -1

    def move(self, s: str, num: int) -> None:
        if s in DIR_NAMES:
            dx, dy = DIR_NAMES[s]
            self.wpx += dx * num
            self.wpy += dy * num
        elif s == "F":
            self.x += self.wpx * num
            self.y += self.wpy * num
        elif s in "LR":
            count = num // 90
            if s == "L":
                count = (4 - count) % 4
            for i in range(count):
                self.wpx, self.wpy = -self.wpy, self.wpx


test = """F10
N3
F7
R90
F11"""
assert Ship1.solve(test) == 25
assert Ship2.solve(test) == 286

text = open("d12/input.txt").read()
print(Ship1.solve(text))
print(Ship2.solve(text))
