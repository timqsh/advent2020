from typing import List, Tuple


def parse(txt: str) -> List[int]:
    return [int(l) for l in txt.splitlines()]


def has_sum_2(nums: List[int], target: int) -> bool:
    # O(K)
    complements = {target - elem for elem in nums}
    return any(elem in complements for elem in nums)


def get_not_summable(nums: List[int], preamble: int = 25) -> Tuple[int, int]:
    # O(N*K)
    for i in range(preamble, len(nums)):
        if not has_sum_2(nums[i - preamble : i], nums[i]):
            return i, nums[i]
    raise RuntimeError("all are summable")


def find_sum_range(nums: List[int], target, final_idx) -> Tuple[int, int]:
    # O(N)
    total = i = j = 0
    while j < final_idx:
        if total == target:
            return i, j
        elif total < target:
            total += nums[j]
            j += 1
        else:  # total > target
            total -= nums[i]
            i += 1
    raise RuntimeError("no sum range")


test = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

assert get_not_summable(parse(test), preamble=5) == (14, 127)
assert find_sum_range(parse(test), target=127, final_idx=14) == (2, 6)


nums = parse(open("d9/input.txt").read())
idx, target = get_not_summable(nums)
print(idx, target)
assert idx == 610
assert target == 552655238

lo, hi = find_sum_range(nums, target, idx)
result = min(nums[lo:hi]) + max(nums[lo:hi])
print(result)
assert result == 70672245
