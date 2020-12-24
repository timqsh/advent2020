import re
from typing import Counter, Set

dirs = [-2, 2, -1 - 1j, 1 - 1j, -1 + 1j, 1 + 1j]
dir_names = "e w ne nw se sw".split()
dir_re = re.compile("|".join(dir_names))
dir_by_name = dict(zip(dir_names, dirs))


def get_black_tiles(txt: str) -> Set[complex]:
    flips = (sum(dir_by_name[d] for d in dir_re.findall(l)) for l in txt.splitlines())
    return {tile for tile, n in Counter(flips).items() if n % 2}


def step(b: Set[complex]) -> Set[complex]:
    near = (tile + delta for tile in b for delta in dirs)
    return {tile for tile, n in Counter(near).items() if n == 2 or n == 1 and tile in b}


def step_n(b: Set[complex], n: int) -> Set[complex]:
    for _ in range(n):
        b = step(b)
    return b


if __name__ == "__main__":
    text = open("d24/input.txt").read()
    task_tiles = get_black_tiles(text)
    print(f"part 1: {len(task_tiles)}")
    print(f"part 2: {len(step_n(task_tiles, 100))}")
