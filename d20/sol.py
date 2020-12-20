import re
from dataclasses import dataclass
from typing import List

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

    def share_border(self, other: "Tile") -> bool:
        for b1 in self.borders():
            for b2 in other.borders():
                if np.array_equal(b1, b2) or np.array_equal(b1[::-1], b2):
                    return True
        return False


def parse_tiles(s: str) -> List[Tile]:
    return [Tile.from_text(b) for b in s.split("\n\n")]


text = open("d20/input.txt").read()
test = open("d20/test.txt").read()

tiles = parse_tiles(text)
for t in tiles:
    print(sum(t.share_border(o) for o in tiles if o is not t))
