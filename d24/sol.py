from typing import Counter, Set, Tuple

Tile = Tuple[int, int]
Board = Set[Tile]


def vec_add(t1: Tile, t2: Tile) -> Tile:
    return t1[0] + t2[0], t1[1] + t2[1]


def get_black_tiles(txt: str) -> Board:
    black_tiles: Board = set()
    for line in txt.splitlines():
        idx = 0
        cur_coord = (0, 0)
        while idx < len(line):
            if line[idx] == "e":
                coord = (-2, 0)
                idx += 1
            elif line[idx] == "w":
                coord = (2, 0)
                idx += 1
            elif line[idx : idx + 2] == "ne":
                coord = (-1, -1)
                idx += 2
            elif line[idx : idx + 2] == "nw":
                coord = (1, -1)
                idx += 2
            elif line[idx : idx + 2] == "se":
                coord = (-1, 1)
                idx += 2
            elif line[idx : idx + 2] == "sw":
                coord = (1, 1)
                idx += 2
            else:
                raise SyntaxError("Wrong coordinate encoding")
            cur_coord = vec_add(cur_coord, coord)
        if cur_coord in black_tiles:
            black_tiles.remove(cur_coord)
        else:
            black_tiles.add(cur_coord)
    return black_tiles


def step(black: Board) -> Board:
    near_count: Counter[Tuple[int, int]] = Counter()
    for tile in black:
        for delta in [
            (-2, 0),
            (2, 0),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
        ]:
            new = vec_add(tile, delta)
            near_count[new] += 1
    new_black = set()
    for tile, count in near_count.items():
        if tile in black and (1 <= count <= 2):
            new_black.add(tile)
        elif tile not in black and count == 2:
            new_black.add(tile)
    return new_black


def step_n(b: Board, n: int) -> Board:
    for _ in range(n):
        b = step(b)
    return b


test = open("d24/test.txt").read()
test_tiles = get_black_tiles(test)
assert len(test_tiles) == 10
assert len(step_n(test_tiles, 100)) == 2208

text = open("d24/input.txt").read()
task_tiles = get_black_tiles(text)
print(f"part 1: {len(task_tiles)}")
part_2 = len(step_n(task_tiles, 100))
print(f"part 2: {part_2}")
