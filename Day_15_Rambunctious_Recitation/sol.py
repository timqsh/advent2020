from collections import defaultdict
from typing import Iterator

from more_itertools import nth, take


def generate(txt: str) -> Iterator[int]:
    yield -1  # idx start from 1
    nums = [int(s) for s in txt.split(",")]
    yield from nums
    turns = defaultdict(list, {elem: [idx + 1] for idx, elem in enumerate(nums)})
    last = nums[-1]
    turn = len(nums) + 1
    while True:
        last_turns = turns[last]
        if len(last_turns) >= 2:
            last = last_turns[-1] - last_turns[-2]
        else:
            last = 0
        yield last
        turns[last].append(turn)
        turn += 1


test = "0,3,6"
result = [-1, 0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
assert take(11, generate(test)) == result

assert nth(generate("1,3,2"), 2020) == 1
assert nth(generate("2,1,3"), 2020) == 10
assert nth(generate("1,2,3"), 2020) == 27
assert nth(generate("2,3,1"), 2020) == 78
assert nth(generate("3,2,1"), 2020) == 438
assert nth(generate("3,1,2"), 2020) == 1836

task = "2,1,10,11,0,6"
print(nth(generate(task), 2020))

# very slow...
# assert nth(generate("0,3,6"), 30000000) == 175594
# assert nth(generate("1,3,2"), 30000000) == 2578
# assert nth(generate("2,1,3"), 30000000) == 3544142
# assert nth(generate("1,2,3"), 30000000) == 261214
# assert nth(generate("2,3,1"), 30000000) == 6895259
# assert nth(generate("3,2,1"), 30000000) == 18
# assert nth(generate("3,1,2"), 30000000) == 362

print(nth(generate(task), 30000000))
