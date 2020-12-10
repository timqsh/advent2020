from collections import Counter
from functools import lru_cache, partial
from itertools import chain, islice, takewhile
from operator import ge
from typing import List

from more_itertools import difference, ilen


def parse(lines: List[str]) -> List[int]:
    return [*map(int, lines)]


def diff_prod(nums: List[int]) -> int:
    """The number of 1 differences times the number of 3 differences"""
    diffs = difference(chain([0], sorted(nums), [max(nums) + 3]))
    count = Counter(diffs)
    return count[1] * count[3]


def arrangements_count(nums: List[int]) -> int:
    """The total number of distinct ways you can arrange the adapters
    to connect the charging outlet to your device"""

    @lru_cache(None)
    def count(i: int) -> int:
        if i == len(nums) - 1:
            return 1
        choices = takewhile(partial(ge, nums[i] + 3), islice(nums, i + 1, None))
        return sum(count(j) for j in range(i + 1, i + 1 + ilen(choices)))

    nums = [0] + sorted(nums)
    return count(0)


def din_prog(nums: List[int]) -> int:
    """Alternative solution to part 2"""
    nums = [0] + sorted(nums)
    dp = Counter({0: 1})
    for n in nums[1:]:
        dp[n] = sum(dp[n - i] for i in range(1, 4))
    return dp[nums[-1]]


lines = open("d10/input.txt").read().splitlines()
test1 = "16 10 15 5 1 11 7 19 6 12 4".split()
test2 = (
    "28 33 18 42 31 14 46 20 48 47 24 23 49 45 "
    "19 38 39 11 1 32 25 35 8 17 7 9 4 2 34 10 3"
).split()

assert diff_prod(parse(test1)) == 35
assert diff_prod(parse(test2)) == 220
result = diff_prod(parse(lines))
print(result)
assert result == 1876

assert arrangements_count(parse(test1)) == 8 == din_prog(parse(test1))
assert arrangements_count(parse(test2)) == 19208 == din_prog(parse(test2))
result = arrangements_count(parse(lines))
print(result)
assert result == 14173478093824 == din_prog(parse(lines))
