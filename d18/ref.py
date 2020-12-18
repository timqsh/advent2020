from operator import add, mul, pow, sub, truediv
from typing import Dict, List, NamedTuple


class Op(NamedTuple):
    precedence: int
    left_assoc: bool


OP = {"+": add, "*": mul, "-": sub, "/": truediv, "^": pow}
OP_NORMAL = {
    "+": Op(1, True),
    "-": Op(1, True),
    "*": Op(2, True),
    "/": Op(2, True),
    "^": Op(3, False),
}
OP_PART_1 = {
    "+": Op(1, True),
    "*": Op(1, True),
}
OP_PART_2 = {
    "+": Op(2, True),
    "*": Op(1, True),
}


def tokenize(s: str) -> List[str]:
    """Returns tokens after lexing given string"""
    s = s.replace("(", " ( ").replace(")", " ) ")
    for op in OP:
        s = s.replace(op, f" {op} ")
    return s.split()


def shunting_yard(tokens: List[str], op_table: Dict[str, Op]) -> List[str]:
    """Returns tokens in Reverse Polish Notation parsed from tokens in infix notation"""
    output_queue: List[str] = []
    stack: List[str] = []
    for t in tokens:
        if t in OP:
            while (
                stack
                and stack[-1] != "("
                and (
                    op_table[t].precedence < op_table[stack[-1]].precedence
                    or op_table[t].precedence == op_table[stack[-1]].precedence
                    and op_table[t].left_assoc
                )
            ):
                t2 = stack.pop()
                output_queue.append(t2)
            stack.append(t)
        elif t == "(":
            stack.append(t)
        elif t == ")":
            while stack[-1] != "(":
                t2 = stack.pop()
                output_queue.append(t2)
            stack.pop()  # delete "(" from stack
        else:  # operand
            output_queue.append(t)
    for op in reversed(stack):
        output_queue.append(op)
    return output_queue


def evaluate(rpn: List[str]) -> int:
    """Evaluate expression in Reverse Polish Notation"""
    stack: List[int] = []
    for t in rpn:
        if t in OP:
            second = stack.pop()
            first = stack.pop()
            result = OP[t](first, second)
            stack.append(result)
        else:
            stack.append(int(t))
    if len(stack) == 1:
        return stack[0]
    raise RuntimeError("Stack isn't 1 element after evaluation")


def solve(s: str, precedence: dict) -> int:
    tokens = tokenize(s)
    rpn = shunting_yard(tokens, precedence)
    result = evaluate(rpn)
    return result


if __name__ == "__main__":
    lines = open("d18/input.txt").readlines()
    print(sum(solve(line, OP_PART_1) for line in lines))
    print(sum(solve(line, OP_PART_2) for line in lines))
