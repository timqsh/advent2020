from collections import deque
from itertools import islice
from typing import Deque, Tuple


def parse_block(block: str) -> Deque[int]:
    return deque([int(i) for i in block.splitlines()[1:]])


def parse(txt: str) -> Tuple[Deque[int], Deque[int]]:
    block_1, block_2 = txt.split("\n\n")
    player1 = parse_block(block_1)
    player2 = parse_block(block_2)
    return player1, player2


def calc_score(d: Deque[int]) -> int:
    return sum(v * (len(d) - i) for i, v in enumerate(d))


def solve_1(txt: str) -> int:
    p1, p2 = parse(txt)
    while p1 and p2:
        c1 = p1.popleft()
        c2 = p2.popleft()
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        elif c2 > c1:
            p2.append(c2)
            p2.append(c1)
        else:
            raise RuntimeError("Ties should not happen")
    non_empty = p1 or p2
    return calc_score(non_empty)


def sub_deque(d: Deque[int], n) -> Deque[int]:
    return deque(islice(d, n))


def solve_2(txt: str) -> int:
    def player_1_won(p1: Deque[int], p2: Deque[int]) -> bool:
        cache = set()
        while p1 and p2:
            if (tuple(p1), tuple(p2)) in cache:
                return True
            cache.add((tuple(p1), tuple(p2)))

            c1 = p1.popleft()
            c2 = p2.popleft()
            if c1 <= len(p1) and c2 <= len(p2):
                first_won = player_1_won(sub_deque(p1, c1), sub_deque(p2, c2))
            else:
                first_won = c1 > c2
            if first_won:
                p1.append(c1)
                p1.append(c2)
            else:
                p2.append(c2)
                p2.append(c1)
        return bool(p1)

    p1, p2 = parse(txt)
    first_won = player_1_won(p1, p2)
    non_empty = p1 if first_won else p2
    return calc_score(non_empty)


test = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
test_inf = """Player 1:
43
19

Player 2:
2
29
14"""
assert solve_1(test) == 306
assert solve_2(test) == 291
assert solve_2(test_inf) > 0
text = open("d22/input.txt").read()
result = solve_1(text)
print(result)
res2 = solve_2(text)
print(res2)
