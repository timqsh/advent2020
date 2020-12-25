from pathlib import Path


def part2(l: str) -> int:
    enumerated = [(i, int(c)) for i, c in enumerate(l.split(",")) if c != "x"]
    a, n = [[*t] for t in zip(*enumerated)]
    for i in range(len(a)):
        a[i] = (n[i] - a[i]) % n[i]

    check = -1
    prev_check = n[0]
    product = n[0]
    for i in range(1, len(a)):
        j = 0
        while True:
            check = prev_check + product * j
            if check % n[i] == a[i]:
                prev_check = check
                break
            j += 1
        product *= n[i]
    return check


assert part2("17,x,13,19") == 3417.0
assert part2("67,7,59,61") == 754018.0
assert part2("67,x,7,59,61") == 779210.0
assert part2("67,7,x,59,61") == 1261476.0
assert part2("1789,37,47,1889") == 1202161486

text = (Path(__file__).parent / "input.txt").read_text()
res2 = part2(text.splitlines()[1])
print(res2)
assert res2 == 600689120448303
