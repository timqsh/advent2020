from itertools import product
from typing import Counter, Set, Tuple

State = Set[Tuple[int, ...]]


def parse(s: str, dim: int) -> State:
    return {
        (x, y) + (0,) * (dim - 2)
        for y, l in enumerate(s.splitlines())
        for x, c in enumerate(l)
        if c == "#"
    }


def next_state_(state: State) -> State:
    count: Counter[Tuple[int, ...]] = Counter()
    for point in state:
        for delta in product([-1, 0, 1], repeat=len(point)):
            if not any(delta):
                continue
            neighbor = tuple((sum(d) for d in zip(point, delta)))
            count[neighbor] += 1
    return {p for p, c in count.items() if c == 3 or c == 2 and p in state}


def next_state(state):
    near = (
        tuple(map(sum, zip(point, delta)))
        for point in state
        for delta in product(range(-1, 2), repeat=len(point))
    )
    return {p for p, c in Counter(near).items() if c == 3 or (p in state and c == 4)}


def solve(state: State) -> int:
    for _ in range(6):
        state = next_state(state)
    return len(state)


test1 = """.#.
..#
###"""
assert solve(parse(test1, dim=3)) == 112
assert solve(parse(test1, dim=4)) == 848
text = open("d17/input.txt").read()
print(solve(parse(text, dim=3)))
print(solve(parse(text, dim=4)))
