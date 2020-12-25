import itertools as it
from copy import deepcopy
from pathlib import Path
from typing import Callable, List


class State(List[List[str]]):
    @property
    def height(self):
        return len(self)

    @property
    def width(self):
        return len(self[0])


def parse(txt: str) -> State:
    return State([list(l) for l in txt.splitlines()])


def neighbors_count(state: State, x: int, y: int) -> int:
    total = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            nx = x + dx
            ny = y + dy
            if nx == x and ny == y:
                continue
            if not 0 <= nx < state.width:
                continue
            if not 0 <= ny < state.height:
                continue
            if state[ny][nx] == "#":
                total += 1
    return total


def neighbors_count_2(state: State, x: int, y: int) -> int:
    dirs = list(it.product([-1, 0, 1], repeat=2))
    dirs.remove((0, 0))
    total = 0
    for dx, dy in dirs:
        nx = x
        ny = y
        while True:
            nx = nx + dx
            ny = ny + dy
            if not 0 <= nx < state.width:
                break
            if not 0 <= ny < state.height:
                break
            if state[ny][nx] == "L":
                break
            if state[ny][nx] == "#":
                total += 1
                break
    return total


def next_state(state: State, seat_tolerance: int, neighbors_func: Callable) -> State:
    new_state = deepcopy(state)
    for y in range(state.height):
        for x in range(state.width):
            if state[y][x] == "L" and neighbors_func(state, x, y) == 0:
                new_state[y][x] = "#"
            elif state[y][x] == "#" and neighbors_func(state, x, y) >= seat_tolerance:
                new_state[y][x] = "L"
    return new_state


def sim(state: State, seat_tolerance: int, neighbors_func: Callable) -> State:
    prev = None
    nex = state
    while nex != prev:
        prev = nex
        nex = next_state(nex, seat_tolerance, neighbors_func)
    return nex


def count_all_occupied(state: State) -> int:
    return sum(c == "#" for row in state for c in row)


test = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
assert count_all_occupied(sim(parse(test), 4, neighbors_count)) == 37
assert count_all_occupied(sim(parse(test), 5, neighbors_count_2)) == 26


text = (Path(__file__).parent / "input.txt").read_text()
state = parse(text)

final = sim(state, 4, neighbors_count)
occupied = count_all_occupied(final)
print(occupied)

final = sim(state, 5, neighbors_count_2)
occupied = count_all_occupied(final)
print(occupied)
