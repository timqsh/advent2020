from typing import List, Tuple

import numpy as np
from numba import njit


# @njit
def move(digs: List[int], cur_idx: int) -> Tuple[List[int], int]:
    lowest = 1  # min(digs)
    highest = len(digs)  # max(digs)
    three = (
        digs[cur_idx + 1 : cur_idx + 4]
        + digs[: cur_idx - len(digs) + 4 if cur_idx - len(digs) + 4 >= 0 else 0]
    )
    cur = digs[cur_idx]
    dest = digs[cur_idx] - 1
    while True:
        if dest < lowest:
            dest = highest
        if dest not in three:
            break
        dest -= 1
    new_digs = (
        digs[
            cur_idx - len(digs) + 4 if cur_idx - len(digs) + 4 >= 0 else 0 : cur_idx + 1
        ]
        + digs[cur_idx + 4 :]
    )
    dest_idx = new_digs.index(dest)
    for elem in three[::-1]:
        new_digs.insert(dest_idx + 1, elem)
    new_idx = (new_digs.index(cur) + 1) % len(digs)
    return new_digs, new_idx


def solve(txt: str, moves: int) -> str:
    digs = [int(i) for i in txt]
    cur_idx = 0
    for _ in range(moves):
        digs, cur_idx = move(digs, cur_idx)

    one_idx = digs.index(1)
    return "".join(str(d) for d in digs[one_idx + 1 :] + digs[:one_idx])


@njit(cache=True)
def move_2(arr: np.ndarray) -> None:
    lowest = 1
    highest = len(arr) - 1
    cur = arr[0]
    f1 = arr[cur]
    f2 = arr[f1]
    f3 = arr[f2]
    dest = cur - 1
    while True:
        if dest < lowest:
            dest = highest
        if dest not in (f1, f2, f3):
            break
        dest -= 1
    arr[cur] = arr[f3]
    tmp = arr[dest]
    arr[dest] = f1
    arr[f3] = tmp
    arr[0] = arr[cur]


@njit(cache=True)
def move_2_n(arr: np.ndarray, n) -> None:
    for i in range(n):
        if i % 10 ** 6 == 0:
            print("iteration #" + str(i))
        move_2(arr)


def solve_2(txt: str, moves: int) -> str:
    digs = [int(i) for i in txt]
    arr = np.zeros(max(digs) + 1, dtype=int)
    arr[0] = digs[0]  # pointer in first elem
    for i in range(len(digs)):
        arr[digs[i]] = digs[(i + 1) % len(digs)]
    for _ in range(moves):
        move_2(arr)

    start = arr[1]
    result = []
    while start != 1:
        result.append(start)
        start = arr[start]
    return "".join(str(d) for d in result)


def part_2(txt: str) -> int:
    digs = [int(i) for i in txt]
    arr = np.zeros(10 ** 6 + 1, dtype=int)
    arr[0] = digs[0]  # pointer in first elem
    for i in range(len(digs)):
        arr[digs[i]] = digs[(i + 1) % len(digs)]
    arr[digs[-1]] = len(digs) + 1
    for i in range(len(digs) + 1, 10 ** 6):
        arr[i] = i + 1
    arr[10 ** 6] = digs[0]
    move_2_n(arr, 10 ** 7)

    f1 = arr[1]
    f2 = arr[f1]
    return f1 * f2


assert solve("389125467", 10) == "92658374"
assert solve("389125467", 100) == "67384529"
result_1 = solve("364289715", 100)
print(f"part 1: {result_1}")
assert result_1 == "98645732"

assert part_2("389125467") == 149245887792
result_2 = part_2("364289715")
print(f"part 2: {result_2}")
assert result_2 == 689500518476
