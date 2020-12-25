DIV = 20201227
INIT = 7


def run_loop(pub, size):
    value = 1
    for _ in range(size):
        value = (value * pub) % DIV
    return value


def get_loop_size(pub: int) -> int:
    value = 1
    i = 0
    while value != pub:
        value = (value * INIT) % DIV
        i += 1
    return i


def solve(card_pub: int, door_pub: int) -> int:
    door_loop_size = get_loop_size(door_pub)
    encryption_key = run_loop(card_pub, door_loop_size)
    return encryption_key


assert solve(5764801, 17807724) == 14897079
print(solve(19774466, 7290641))
