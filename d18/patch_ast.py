from ast import Add, BinOp, Expression, Mult, Sub, parse


def replace_ops_1(node):
    if isinstance(node, BinOp) and isinstance(node.op, Sub):
        node.op = Mult(left=replace_ops_1(node.left), right=replace_ops_1(node.right))
    elif isinstance(node, BinOp) and isinstance(node.op, Add):
        node.op = Add(left=replace_ops_1(node.left), right=replace_ops_1(node.right))


def replace_ops_2(node):
    if isinstance(node, BinOp) and isinstance(node.op, Add):
        node.op = Mult(left=replace_ops_2(node.left), right=replace_ops_2(node.right))
    elif isinstance(node, BinOp) and isinstance(node.op, Mult):
        node.op = Add(left=replace_ops_2(node.left), right=replace_ops_2(node.right))


def solve(part, s):
    if part == 1:
        s = s.replace("*", "-")
    else:
        s = s.replace("+", "tmp").replace("*", "+").replace("tmp", "*")

    module = parse(s)
    bin_op = module.body[0].value
    if part == 1:
        replace_ops_1(bin_op)
    else:
        replace_ops_2(bin_op)

    exe = compile(Expression(body=bin_op), filename="", mode="eval")
    val = eval(exe)
    return val


if __name__ == "__main__":
    lines = open("d18/input.txt").read().splitlines()
    print(sum(solve(1, l) for l in lines))
    print(sum(solve(2, l) for l in lines))
