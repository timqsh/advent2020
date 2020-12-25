import re
from pathlib import Path
from typing import Dict, List, Set, Tuple


def parse_line(l: str) -> Tuple[List[str], List[str]]:
    if m := re.match(r"^([\w ]+) \(contains ([\w, ]+)\)", l):
        ingredients_str, allergens_str = m.groups()
        i = ingredients_str.split()
        a = allergens_str.split(", ")
        return i, a
    raise ValueError(f"Can't parse line {l}")


def parse(txt: str) -> Tuple[Dict[str, Set[str]], Set[str]]:
    lines = txt.splitlines()
    possible_ingredients_for_allergen: Dict[str, Set[str]] = {}
    all_ingredient: Set[str] = set()
    for l in lines:
        ingredients, allergens = parse_line(l)
        all_ingredient |= set(ingredients)
        for a in allergens:
            if a not in possible_ingredients_for_allergen:
                possible_ingredients_for_allergen[a] = set(ingredients)
            else:
                possible_ingredients_for_allergen[a] &= set(ingredients)
    return possible_ingredients_for_allergen, all_ingredient


test = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

test_result = """kfcds nhms sbzzf trh"""

text = (Path(__file__).parent / "input.txt").read_text()

might_contain, all_ingredient = parse(text)
definitely_contain: Dict[str, str] = {}
while might_contain:
    contain_one = [(k, v) for k, v in might_contain.items() if len(v) == 1]
    if not contain_one:
        raise RuntimeError("Can't deduce solution")
    first = contain_one[0]
    k, set_of_one = first
    v = next(iter(set_of_one))
    del might_contain[k]
    for elem in might_contain:
        if v in might_contain[elem]:
            might_contain[elem].remove(v)
    definitely_contain[v] = k

dont_contain = all_ingredient - set(definitely_contain)

total = 0
all_list = [parse_line(l) for l in text.splitlines()]
for ingredients, allergens in all_list:
    total += sum(i in dont_contain for i in ingredients)
print(total)
assert total == 2162
part2 = ",".join(sorted(definitely_contain, key=definitely_contain.get))  # type: ignore
print(part2)
assert part2 == "lmzg,cxk,bsqh,bdvmx,cpbzbx,drbm,cfnt,kqprv"
