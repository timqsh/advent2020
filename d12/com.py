def rotate(s: complex, side: str, deg: int) -> complex:
    return s * 1j ** (deg // 90 if side == "R" else -deg // 90)


def move(compass: str, val=1) -> complex:
    return val * 1j ** "ESWN".index(compass)


def solve(txt: str, part: int) -> int:
    instructions = [(l[0], int(l[1:])) for l in txt.splitlines()]
    speed = move("E") if part == 1 else move("E", 10) + move("N")
    pos = 0 + 0j
    for act, val in instructions:
        if act in "ESWN":
            if part == 1:
                pos += move(act, val)
            else:
                speed += move(act, val)
        elif act == "F":
            pos += speed * val
        elif act in "LR":
            speed = rotate(speed, act, val)
    return int(abs(pos.real) + abs(pos.imag))


test = """F10
N3
F7
R90
F11"""
assert solve(test, 1) == 25
assert solve(test, 2) == 286

text = open("d12/input.txt").read()
result1 = solve(text, 1)
print(result1)
assert result1 == 508
result2 = solve(text, 2)
print(result2)
assert result2 == 30761
