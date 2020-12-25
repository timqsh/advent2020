from Day_23_Crab_Cups.sol import part_1, part_2


def test_part_1():
    assert part_1("389125467", 10) == "92658374"
    assert part_1("389125467", 100) == "67384529"
    result_1 = part_1("364289715", 100)
    assert result_1 == "98645732"


def test_part_2():
    assert part_2("389125467") == 149245887792
    result_2 = part_2("364289715")
    assert result_2 == 689500518476
