import re
from pathlib import Path
from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError, validator

T = TypeVar("T", bound="Passport")


class Passport(BaseModel):
    byr: int
    iyr: int
    eyr: int
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[str] = None

    @classmethod
    def from_string(cls: Type[T], s: str) -> T:
        fields = re.split(r"\s", s.strip())
        d = {}
        for f in fields:
            key, value = f.split(":")
            d[key] = value
        return cls(**d)


class ValidPassport(Passport):
    class Meta:
        ALLOWED_COLORS = "amb blu brn gry grn hzl oth".split()
        RE_YEAR = re.compile(r"^\d{4}$")
        RE_HGT = re.compile(r"^(\d+)(cm|in)$")
        RE_HCL = re.compile(r"^#[0-9a-f]{6}$")
        RE_PID = re.compile(r"^[0-9]{9}$")

    @validator("byr", "iyr", "eyr", pre=True)
    def is_year(cls, v: str):
        if not cls.Meta.RE_YEAR.match(v):
            raise ValueError(f"{v} is not valid year")
        return v

    @staticmethod
    def check_range(v: int, lo: int, hi: int) -> None:
        if not lo <= v <= hi:
            raise ValueError(f"must be between {lo} and {hi}")

    @validator("byr")
    def check_byr(cls, v: int):
        cls.check_range(v, 1920, 2002)
        return v

    @validator("iyr")
    def iyr_valid_(cls, v: int):
        cls.check_range(v, 2010, 2020)
        return v

    @validator("eyr")
    def eyr_valid_(cls, v: int):
        cls.check_range(v, 2020, 2030)
        return v

    @validator("hgt")
    def hgt_valid_(cls, v: str):
        m = cls.Meta.RE_HGT.match(v)
        if not m:
            raise ValueError("must be a number in `cm` or `in`")
        value, unit = m.groups()
        if unit == "cm":
            lo, hi = 150, 193
        else:
            lo, hi = 59, 76
        cls.check_range(int(value), lo, hi)
        return v

    @validator("hcl")
    def hcl_valid(cls, v: str):
        if not cls.Meta.RE_HCL.match(v):
            raise ValueError(f"{v} doesn't match format #HEX")
        return v

    @validator("ecl")
    def ecl_valid(cls, v: str):
        if v not in cls.Meta.ALLOWED_COLORS:
            raise ValueError(f"should be on of {cls.Meta.ALLOWED_COLORS}")
        return v

    @validator("pid")
    def pid_valid(cls, v: str):
        if not cls.Meta.RE_PID.match(v):
            raise ValueError("must be 9 digits")
        return v


lines = (Path(__file__).parent / "input.txt").read_text().split("\n\n")

passwords: List[Passport] = []
valid_passwords: List[ValidPassport] = []
for line in lines:
    try:
        passwords.append(Passport.from_string(line))
        valid_passwords.append(ValidPassport.from_string(line))
    except ValidationError as e:
        print(e)
        pass
print(f"{len(passwords) = } {len(valid_passwords) = }")
