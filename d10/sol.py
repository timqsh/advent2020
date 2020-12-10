import functools

text = open("d10/input.txt").read()
test = """16
10
15
5
1
11
7
19
6
12
4"""
test2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""


@functools.lru_cache(None)
def count(i: int) -> int:
    if nums[i] == maximum:
        return 1
    choices = []
    for j in range(i + 1, len(nums)):
        if nums[j] <= nums[i] + 3:
            choices.append(j)
    return sum(count(a) for a in choices)


nums = [int(l) for l in text.split()]
maximum = max(nums)
nums = sorted(nums)
diff = 0
curr = 0
ones = 0
threes = 0
for n in nums:
    if n == curr + 1:
        ones += 1
    if n == curr + 3:
        threes += 1
    curr = n

# print(ones)
# print(threes)
print(ones * (threes + 1))

total = 0
cur = 0
while True:
    if nums[cur] > 3:
        break
    total += count(cur)
    cur += 1
# print(count(0))
print(total)
