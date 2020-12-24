import pytest

from d24.sol import get_black_tiles, step_n


@pytest.fixture(scope="module")
def example_data():
    return open("d24/test.txt").read()


@pytest.fixture(scope="module")
def task_data():
    return open("d24/input.txt").read()


def test_example(example_data):
    test_tiles = get_black_tiles(example_data)
    assert len(test_tiles) == 10
    assert len(step_n(test_tiles, 100)) == 2208


def test_task(task_data):
    task_tiles = get_black_tiles(task_data)
    assert len(task_tiles) == 450
    assert len(step_n(task_tiles, 100)) == 4059
