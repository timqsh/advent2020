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
        first, *rest = txt.splitlines()
        assert (m := re.match(r"Tile (\d+):", first))
        id = int(m.group(1))
        data = parse_array(rest)
        return cls(id, data)


def parse_tiles(s: str) -> List[Tile]:
    return [Tile.from_text(b) for b in s.split("\n\n")]


def parse_array(lines: List[str]) -> np.array:
    d = {"#": 1, ".": 0}
    li = [[d[c] for c in l] for l in lines]
    return np.array(li)


def borders(m: np.array) -> List[np.array]:
    return [m[0], m[-1], m[:, 0], m[:, -1]]


def same_border(b1: np.array, b2: np.array) -> bool:
    return np.array_equal(b1, b2) or np.array_equal(b1[::-1], b2)


def have_border(matrix: np.array, border: np.array) -> bool:
    return any(same_border(border, b) for b in borders(matrix))


def share_border(m1: np.array, m2: np.array) -> bool:
    return any(have_border(m1, b) for b in borders(m2))


def no_borders(m: np.array) -> np.array:
    return m[1:-1, 1:-1]


def orientations(m: np.array) -> Iterator[np.array]:
    for _ in range(2):
        for _ in range(4):
            yield m
            m = np.rot90(m)
        m = np.fliplr(m)


def get_tiles_array(tiles: List[np.array]) -> np.array:
    tiles_copy = tiles[:]
    n = int(math.sqrt(len(tiles_copy)))
    tiles_array = np.zeros((n, n), dtype=object)

    # 1. Find square tile for upper left corner (should have 2 borders)
    for t in tiles_copy:
        if sum(share_border(t.data, o.data) for o in tiles_copy if o is not t) == 2:
            first = t
            tiles_copy.remove(t)
            break
    else:
        raise RuntimeError("Can't find corner")

    # 2. Orient first tile so that it has shared borders on right and down
    for oriented in orientations(first.data):
        have_bottom = any(have_border(t.data, oriented[-1]) for t in tiles_copy)
        have_right = any(have_border(t.data, oriented[:, -1]) for t in tiles_copy)
        if have_bottom and have_right:
            first.data = oriented
            break
    else:
        raise RuntimeError("Can't rotate corner")
    tiles_array[0, 0] = first

    # 3. Fill top row left to right
    for x in range(1, n):
        for t in tiles_copy:
            found = False
            for oriented in orientations(t.data):
                prev_right_border = tiles_array[0, x - 1].data[:, -1]
                cur_left_border = oriented[:, 0]
                if np.array_equal(prev_right_border, cur_left_border):
                    t.data = oriented
                    tiles_array[0, x] = t
                    tiles_copy.remove(t)
                    found = True
                    break
            if found:
                break
        else:
            raise RuntimeError("Can't fill top row")

    # 4. Fill other rows up to down
    for y in range(1, n):
        for x in range(n):
            for t in tiles_copy:
                found = False
                for oriented in orientations(t.data):
                    prev_bottom_border = tiles_array[y - 1, x].data[-1]
                    cur_top_border = oriented[0]
                    if np.array_equal(prev_bottom_border, cur_top_border):
                        t.data = oriented
                        tiles_array[y, x] = t
                        tiles_copy.remove(t)
                        found = True
                        break
                if found:
                    break
            else:
                raise RuntimeError("Can't fill bottom rows")

    return tiles_array


def part_1(txt: str) -> int:
    tiles = parse_tiles(txt)
    tiles_array = get_tiles_array(tiles)
    return (
        tiles_array[0, 0].id
        * tiles_array[-1, 0].id
        * tiles_array[-1, -1].id
        * tiles_array[0, -1].id
    )


def part_2(txt: str) -> int:
    tiles = parse_tiles(txt)
    n = int(math.sqrt(len(tiles)))
    tile_n = len(tiles[0].data)
    no_border_n = tile_n - 2
    combined_n = no_border_n * n
    tiles_array = get_tiles_array(tiles)

    combined = np.zeros((combined_n, combined_n))
    for y in range(n):
        for x in range(n):
            combined[
                y * no_border_n : y * no_border_n + no_border_n,
                x * no_border_n : x * no_border_n + no_border_n,
            ] = no_borders(tiles_array[y, x].data)

    monster_pattern = """..................#.
#....##....##....###
.#..#..#..#..#..#..."""
    monster = parse_array(monster_pattern.splitlines())
    monster_height, monster_width = monster.shape

    def is_monster(slice: np.array) -> bool:
        return np.sum(slice - monster == -1) == 0

    monster_count = 0
    for o in orientations(combined):
        for y in range(combined_n - monster_height + 1):
            for x in range(combined_n - monster_width + 1):
                monster_count += is_monster(
                    o[y : y + monster_height, x : x + monster_width]
                )

    roughness = np.sum(combined == 1) - np.sum(monster == 1) * monster_count
    return roughness


def main():
    test = open("d20/test.txt").read()
    text = open("d20/input.txt").read()
    assert part_1(test) == 20899048083289
    result_1 = part_1(text)
    print(result_1)
    assert result_1 == 29584525501199

    assert part_2(test) == 273
    result_2 = part_2(text)
    print(result_2)
    assert result_2 == 1665


if __name__ == "__main__":
    main()
