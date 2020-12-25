import pytest

from Day_18_Operation_Order.patch_ast import solve as ast_solve
from Day_18_Operation_Order.ref import OP_NORMAL, OP_PART_1, OP_PART_2, solve

normal_data = [
    ("2+2", 4),
    ("1+2+3", 6),
    ("3-1", 2),
    ("3-2-1", 0),
    ("2^3", 8),
    ("2^3^2", 512),
    ("2+2*2^3+1", 19),
    ("(2+2)*2", 8),
    ("100-((100-98-1)*2)-((2*5)^2-2)-1-1-1", -3),
    ("24/2/3/2", 2.0),
]


@pytest.mark.parametrize("string, result", normal_data)
def test_solve_normal(string, result):
    assert solve(string, OP_NORMAL) == result


data_1 = [
    ("1 + 2 * 3 + 4 * 5+ 6", 71),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 26),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
]


@pytest.mark.parametrize("string, result", data_1)
def test_solve_1(string, result):
    assert solve(string, OP_PART_1) == result


@pytest.mark.parametrize("string, result", data_1)
def test_solve_ast_1(string, result):
    assert ast_solve(1, string) == result


data_2 = [
    ("1 + 2 * 3 + 4 * 5 + 6", 231),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 46),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
]


@pytest.mark.parametrize("string, result", data_2)
def test_solve_2(string, result):
    assert solve(string, OP_PART_2) == result


@pytest.mark.parametrize("string, result", data_2)
def test_solve_ast_2(string, result):
    assert ast_solve(2, string) == result
