from pathlib import Path

LINES = (Path(__file__).parent / "input.txt").read_text().splitlines()
WIDTH = len(LINES[0])

result = 1
for (right, down) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    trees_count = vertical = horizontal = 0
    while vertical < len(LINES):
        if LINES[vertical][horizontal] == "#":
            trees_count += 1
        horizontal = (horizontal + right) % WIDTH
        vertical += down
    result *= trees_count
    print(trees_count)
print(result)
