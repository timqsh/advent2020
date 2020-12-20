import pytest

from d1.sol import part_1, part_2


def test_part_1():
    assert part_1([2019, 1]) == 2019


def test_part_2():
    assert part_2([2000, 19, 1]) == 2000 * 19


def test_no_sum():
    with pytest.raises(ValueError):
        part_1([1, 2, 3])
