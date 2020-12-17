from copy import deepcopy
from itertools import product
from typing import List


class Cube3(List[List[List[str]]]):
    depth = 13

    @property
    def height(self) -> int:
        return len(self[0])

    @property
    def width(self) -> int:
        return len(self[0][0])

    @classmethod
    def from_string(cls, s: str) -> "Cube3":
        d = 6
        first_frame = [list("." * d + l + "." * d) for l in s.splitlines()]
        width = len(first_frame[0])
        for _ in range(d):
            first_frame.append(list("." * width))
        for _ in range(d):
            first_frame.insert(0, list("." * width))
        height = len(first_frame)
        other_frames = [[["."] * width for _ in range(height)] for _ in range(d)]
        other_frames_2 = deepcopy(other_frames)
        return Cube3([*other_frames_2, first_frame, *other_frames])

    def active_count(self) -> int:
        total = 0
        for x, y, z in product(
            range(self.width), range(self.height), range(self.depth)
        ):
            if self[z][y][x] == "#":
                total += 1
        return total

    def active_neighbors_count(self, x, y, z) -> int:
        directions = [d for d in product([-1, 0, 1], repeat=3) if d != (0, 0, 0)]
        total = 0
        for dx, dy, dz in directions:
            if (
                (0 <= x + dx < self.width)
                and (0 <= y + dy < self.height)
                and (0 <= z + dz < self.depth)
                and self[z + dz][y + dy][x + dx] == "#"
            ):
                total += 1
        return total

    def next_state(self) -> "Cube3":
        nex = deepcopy(self)
        for x, y, z in product(
            range(self.width), range(self.height), range(self.depth)
        ):
            nc = self.active_neighbors_count(x, y, z)
            if self[z][y][x] == "#" and nc in [2, 3]:
                nex[z][y][x] = "#"
            elif self[z][y][x] == "." and nc == 3:
                nex[z][y][x] = "#"
            else:
                nex[z][y][x] = "."
        return nex

    def simulate(self) -> int:
        for _ in range(6):
            self = self.next_state()
        return self.active_count()

    def __repr__(self) -> str:
        result = ""
        for z in range(self.depth):
            result += f"z={z}\n"
            for y in range(self.height):
                result += "".join(self[z][y]) + "\n"
            result += "\n"
        return result


class Cube4(List[List[List[List[str]]]]):
    depth = 13
    fourth = 13

    @property
    def height(self) -> int:
        return len(self[0][0])

    @property
    def width(self) -> int:
        return len(self[0][0][0])

    @classmethod
    def from_string(cls, s: str) -> "Cube4":
        d = 6
        first_frame = [list("." * d + l + "." * d) for l in s.splitlines()]
        width = len(first_frame[0])
        for _ in range(d):
            first_frame.append(list("." * width))
        for _ in range(d):
            first_frame.insert(0, list("." * width))
        height = len(first_frame)
        other_frames = [[["."] * width for _ in range(height)] for _ in range(d)]
        other_frames_2 = deepcopy(other_frames)
        other_four = [
            [[["."] * width for _ in range(height)] for _ in range(d * 2 + 1)]
            for _ in range(d)
        ]
        other_four_2 = deepcopy(other_four)
        return Cube4(
            [*other_four, [*other_frames_2, first_frame, *other_frames], *other_four_2]
        )

    def active_count(self) -> int:
        total = 0
        for x, y, z, w in product(
            range(self.width), range(self.height), range(self.depth), range(self.fourth)
        ):
            if self[w][z][y][x] == "#":
                total += 1
        return total

    def active_neighbors_count(self, x, y, z, w) -> int:
        directions = [d for d in product([-1, 0, 1], repeat=4) if d != (0, 0, 0, 0)]
        total = 0
        for dx, dy, dz, dw in directions:
            if (
                (0 <= x + dx < self.width)
                and (0 <= y + dy < self.height)
                and (0 <= z + dz < self.depth)
                and (0 <= w + dw < self.fourth)
                and self[w + dw][z + dz][y + dy][x + dx] == "#"
            ):
                total += 1
        return total

    def next_state(self) -> "Cube4":
        nex = deepcopy(self)
        for x, y, z, w in product(
            range(self.width), range(self.height), range(self.depth), range(self.fourth)
        ):
            nc = self.active_neighbors_count(x, y, z, w)
            if self[w][z][y][x] == "#" and nc in [2, 3]:
                nex[w][z][y][x] = "#"
            elif self[w][z][y][x] == "." and nc == 3:
                nex[w][z][y][x] = "#"
            else:
                nex[w][z][y][x] = "."
        return nex

    def simulate(self) -> int:
        for _ in range(6):
            self = self.next_state()
        return self.active_count()


test1 = """.#.
..#
###"""
assert Cube3.from_string(test1).simulate() == 112
assert Cube4.from_string(test1).simulate() == 848

text = open("d17/input.txt").read()
cube = Cube3.from_string(text)
part1 = cube.simulate()
print(part1)
assert part1 == 306
print(Cube4.from_string(text).simulate())
