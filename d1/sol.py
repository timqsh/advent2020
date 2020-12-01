import itertools as it
import operator
from functools import reduce
from pathlib import Path
from typing import List


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def prod_of_2020_sum(nums: List[int], n: int) -> int:
    try:
        return next(prod(c) for c in it.combinations(nums, n) if sum(c) == 2020)
    except StopIteration:
        raise ValueError("There are no numbers with sum=2020")


def part_1(nums: List[int]) -> int:
    return prod_of_2020_sum(nums, 2)


def part_2(nums: List[int]) -> int:
    return prod_of_2020_sum(nums, 3)


def read_input_text() -> str:
    input_file = Path(__file__).parent / "input.txt"
    return input_file.read_text()


def parse_input(text: str) -> List[int]:
    return [int(s) for s in text.splitlines()]


def main() -> None:
    input_text = read_input_text()
    nums = parse_input(input_text)

    result_1 = part_1(nums)
    print(f"{result_1=}")

    result_2 = part_2(nums)
    print(f"{result_2=}")


if __name__ == "__main__":
    main()
