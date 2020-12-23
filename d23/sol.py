import numpy as np
from numba import njit


@njit(cache=True)
def move(arr: np.ndarray) -> None:
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
def move_n(arr: np.ndarray, n) -> None:
    for i in range(n):
        if i % 10 ** 6 == 0:
            print("iteration #" + str(i))
        move(arr)


def part_1(txt: str, moves: int) -> str:
    digs = [int(i) for i in txt]
    arr = np.zeros(max(digs) + 1, dtype=int)
    arr[0] = digs[0]  # pointer in first elem
    for i in range(len(digs)):
        arr[digs[i]] = digs[(i + 1) % len(digs)]
    for _ in range(moves):
        move(arr)

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
    move_n(arr, 10 ** 7)

    f1 = arr[1]
    f2 = arr[f1]
    return f1 * f2


if __name__ == "__main__":
    result_1 = part_1("364289715", 100)
    print(f"part 1: {result_1}")

    result_2 = part_2("364289715")
    print(f"part 2: {result_2}")
