from functools import partial

from d18.ref import OP_NORMAL, OP_PART_1, OP_PART_2, solve


def test_solve_normal():
    solve_norm = partial(solve, precedence=OP_NORMAL)
    assert solve_norm("2+2") == 4
    assert solve_norm("1+2+3") == 6
    assert solve_norm("3-1") == 2
    assert solve_norm("3-2-1") == 0
    assert solve_norm("2^3") == 8
    assert solve_norm("2^3^2") == 512
    assert solve_norm("2+2*2^3+1") == 19
    assert solve_norm("(2+2)*2") == 8
    assert solve_norm("100-((100-98-1)*2)-((2*5)^2-2)-1-1-1") == -3
    assert solve_norm("24/2/3/2") == 2.0


def test_solve_1():
    solve_1 = partial(solve, precedence=OP_PART_1)
    assert solve_1("1 + 2 * 3 + 4 * 5+ 6") == 71
    assert solve_1("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert solve_1("2 * 3 + (4 * 5)") == 26
    assert solve_1("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    assert solve_1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert solve_1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632


def test_solve_2():
    solve_2 = partial(solve, precedence=OP_PART_2)
    assert solve_2("1 + 2 * 3 + 4 * 5 + 6") == 231
    assert solve_2("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert solve_2("2 * 3 + (4 * 5)") == 46
    assert solve_2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert solve_2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert solve_2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
