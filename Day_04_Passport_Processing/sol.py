import re
from pathlib import Path
from typing import Dict, List

lines = (Path(__file__).parent / "input.txt").read_text().split("\n\n")

passwords: List[Dict[str, str]] = []
for line in lines:
    fields = re.split(r"\s", line.strip())
    d = {}
    for f in fields:
        key, value = f.split(":")
        d[key] = value
    passwords.append(d)

keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]  # "cid"

count1 = 0
count2 = 0
for pwd in passwords:
    if not all(k in pwd for k in keys):
        continue
    count1 += 1

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not (1920 <= int(pwd["byr"]) <= 2002):
        continue
    if not (2010 <= int(pwd["iyr"]) <= 2020):
        continue
    if not (2020 <= int(pwd["eyr"]) <= 2030):
        continue

    # hgt (Height) - a number followed by either cm or in:
    # If cm, the number must be at least 150 and at most 193.
    # If in, the number must be at least 59 and at most 76.
    h = pwd["hgt"]
    if h.endswith("cm"):
        if not (150 <= int(h[:-2]) <= 193):
            continue
    elif h.endswith("in"):
        if not (59 <= int(h[:-2]) <= 76):
            continue
    else:
        continue

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if not re.match(r"^#[0-9a-f]{6}$", pwd["hcl"]):
        continue

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if pwd["ecl"] not in "amb blu brn gry grn hzl oth".split():
        continue

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not re.match(r"^[0-9]{9}$", pwd["pid"]):
        continue

    # cid (Country ID) - ignored, missing or not.
    # pass
    count2 += 1

print(f"{count1 = } {count2 = }")
