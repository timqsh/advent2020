from dataclasses import dataclass
from typing import List, NamedTuple


class Instruction(NamedTuple):
    action: str
    value: int


def parse(txt: str) -> List[Instruction]:
    return [Instruction(l[0], int(l[1:])) for l in txt.splitlines()]


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other) -> "Vector":
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __mul__(self, num) -> "Vector":
        if isinstance(num, int):
            return Vector(self.x * num, self.y * num)
        return NotImplemented

    def rotate_90_right(self) -> "Vector":
        return Vector(self.y, -self.x)

    def rotate(self, side: str, deg: int) -> "Vector":
        count = deg // 90
        if side == "L":
            count = 4 - count
        new = self
        for _ in range(count):
            new = new.rotate_90_right()
        return new


# Start from East, rotate Clockwise
DIRS = [Vector(1, 0)]
for i in range(3):
    DIRS.append(DIRS[i].rotate_90_right())
DIR_NAMES = dict(zip("ESWN", DIRS))


def from_compass(direction: str, value=1) -> "Vector":
    return DIR_NAMES[direction] * value


@dataclass
class BaseShip:
    pos: Vector = Vector(0, 0)

    def move(self, instruction: Instruction) -> None:
        raise NotImplementedError

    def run(self, instructions: List[Instruction]) -> None:
        for ins in instructions:
            self.move(ins)

    @classmethod
    def solve(cls, txt: str) -> int:
        instructions = parse(txt)
        obj = cls()
        obj.run(instructions)
        return obj.manhatten()

    def manhatten(self) -> int:
        return abs(self.pos.x) + abs(self.pos.y)


@dataclass
class Ship1(BaseShip):
    direction: Vector = from_compass("E")

    def move(self, instruction: Instruction) -> None:
        act, val = instruction
        if act in "ESWN":
            self.pos += from_compass(act, val)
        elif act == "F":
            self.pos += self.direction * val
        elif act in "LR":
            self.direction = self.direction.rotate(act, val)


@dataclass
class Ship2(BaseShip):
    way_point: Vector = from_compass("E", 10) + from_compass("N", 1)

    def move(self, instruction: Instruction) -> None:
        act, val = instruction
        if act in "ESWN":
            self.way_point += from_compass(act, val)
        elif act == "F":
            self.pos += self.way_point * val
        elif act in "LR":
            self.way_point = self.way_point.rotate(act, val)


test = """F10
N3
F7
R90
F11"""
assert Ship1.solve(test) == 25
assert Ship2.solve(test) == 286

text = open("d12/input.txt").read()
result1 = Ship1.solve(text)
print(result1)
assert result1 == 508
result2 = Ship2.solve(text)
print(result2)
assert result2 == 30761
