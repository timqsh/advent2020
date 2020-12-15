from itertools import count
from typing import Iterator, List

from more_itertools import nth, take


def game(nums: List[int]) -> Iterator[int]:
    yield from nums
    seen = {n: i for i, n in enumerate(nums)}
    last = -1
    for i in count(len(nums) - 1):
        diff = i - seen.get(last, i)
        yield diff
        seen[last] = i
        last = diff


def game_nth_turn(nums: List[int], n: int) -> int:
    return nth(game(nums), n - 1)  # type: ignore


assert take(10, game([0, 3, 6])) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
assert game_nth_turn([1, 3, 2], 2020) == 1
assert game_nth_turn([2, 1, 3], 2020) == 10
assert game_nth_turn([1, 2, 3], 2020) == 27
assert game_nth_turn([2, 3, 1], 2020) == 78
assert game_nth_turn([3, 2, 1], 2020) == 438
assert game_nth_turn([3, 1, 2], 2020) == 1836

task = [2, 1, 10, 11, 0, 6]
print(game_nth_turn(task, 2020))
print(game_nth_turn(task, 30000000))
