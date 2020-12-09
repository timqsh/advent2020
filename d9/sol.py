import itertools as it

text = open("d9/input.txt").read()
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

preamble = 25
nums = [int(l) for l in text.splitlines()]
for i in range(preamble + 1, len(nums)):
    if not any(sum(t) == nums[i] for t in it.combinations(nums[i - preamble : i], 2)):
        print(i, nums[i])

idx, target = 610, 552655238
for i in range(idx):
    for j in range(i + 1, idx):
        d = nums[i:j]
        if sum(d) == target:
            print(min(d) + max(d))
