import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Password:
    pattern = re.compile(r"(\d+)\-(\d+) (.): (.*)")
    times_min: int
    times_max: int
    letter: str
    password: str

    @classmethod
    def parse_string(cls, line: str) -> "Password":
        if m := cls.pattern.match(line):
            return cls(int(m.group(1)), int(m.group(2)), m.group(3), m.group(4))
        raise ValueError(f"{line} doesn't match pattern")

    def is_valid(self) -> bool:
        return self.times_min <= self.password.count(self.letter) <= self.times_max

    def is_valid_2(self) -> bool:
        c1 = self.password[self.times_min - 1]
        c2 = self.password[self.times_max - 1]
        return (c1 == self.letter) ^ (c2 == self.letter)


lines = (Path(__file__).parent / "input.txt").read_text().splitlines()

passwords = [Password.parse_string(line) for line in lines]
result1 = sum(p.is_valid() for p in passwords)
result2 = sum(p.is_valid_2() for p in passwords)
print(f"{result1=} {result2=}")
