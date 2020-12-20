import math
import re
from dataclasses import dataclass
from typing import Iterator, List

import numpy as np


@dataclass
class Tile:
    id: int
    data: np.array

    @classmethod
    def from_text(cls, txt: str) -> "Tile":
        lines = txt.splitlines()
        assert (m := re.match(r"Tile (\d+):", lines[0]))
        id = int(m.group(1))
        d = {"#": 1, ".": 0}
        li = [[d[c] for c in l] for l in lines[1:]]
        return cls(id, np.array(li))

    def borders(self) -> List[np.array]:
        d = self.data
        return [d[0], d[-1], d[:, 0], d[:, -1]]

    def have_border(self, border: np.array) -> bool:
        for b in self.borders():
            if np.array_equal(b, border) or np.array_equal(b[::-1], border):
                return True
        return False

    def share_border(self, other: "Tile") -> bool:
        for b1 in self.borders():
            for b2 in other.borders():
                if np.array_equal(b1, b2) or np.array_equal(b1[::-1], b2):
                    return True
        return False

    def orientations(self) -> Iterator["Tile"]:
        for _ in range(2):
            for _ in range(4):
                yield self
                self.data = np.rot90(self.data)
            self.data = np.fliplr(self.data)


def parse_tiles(s: str) -> List[Tile]:
    return [Tile.from_text(b) for b in s.split("\n\n")]


text = open("d20/input.txt").read()
test = open("d20/test.txt").read()
tiles = parse_tiles(test)
n = int(math.sqrt(len(tiles)))

# 1. Find square tile for upper left corner
for t in tiles:
    if sum(t.share_border(o) for o in tiles if o is not t) == 2:
        first = t
        tiles.remove(t)
        break
else:
    raise RuntimeError

# 2. Orient first tile so that it has shared borders on right and down
for o in first.orientations():
    if any(t.have_border(o.data[-1]) for t in tiles) and any(
        t.have_border(o.data[:, -1]) for t in tiles
    ):
        orientation = o
        break
else:
    raise RuntimeError

final_map = np.zeros((n, n), dtype=object)
final_map[0, 0] = orientation

# 3. Fill top row left to right
prev = orientation
for i in range(1, n):
    for t in tiles:
        found = False
        for o in t.orientations():
            if np.array_equal(prev.data[:, -1], t.data[:, 0]):
                final_map[0, i] = t
                prev = t
                tiles.remove(t)
                found = True
                break
        if found:
            break
    else:
        raise RuntimeError

# print(final_map)

# 4. Fill other rows up to down
for y in range(1, n):
    for x in range(n):
        prev = final_map[y - 1, x]
        for t in tiles:
            found = False
            for o in t.orientations():
                if np.array_equal(prev.data[-1], o.data[0]):
                    final_map[y, x] = o
                    tiles.remove(t)
                    found = True
                    break
            if found:
                break
        else:
            raise RuntimeError

print(final_map)
