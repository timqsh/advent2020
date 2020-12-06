txt_blocks = open("d6/input.txt").read().split("\n\n")
groups = [[set(l) for l in block.splitlines()] for block in txt_blocks]

def count_groups(groups, combine_strategy):
    return sum(len(combine_strategy(*g)) for g in groups)

count_if_any = count_groups(groups, set.union)
count_if_all = count_groups(groups, set.intersection)
print(f"{count_if_any = } {count_if_all = }")
