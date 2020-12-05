lines = open("d5/input.txt").read().splitlines()

ids = sorted(int(l.translate(str.maketrans("BFRL", "1010")), 2) for l in lines)
print(f"max: {ids[-1]}")
for i in range(1, len(ids)):
    if ids[i] - ids[i - 1] == 2:
        print(f"missing: {ids[i] - 1}")
