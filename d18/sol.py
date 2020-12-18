PLUS = "+"
TIMES = "*"
LPAREN = "("
RPAREN = ")"
EOF = "EOF"


class ArithmeticParser:
    """Parses a token list and returns a nested expression structure in
    prefix form using recursive descent method.

    Code based on this example:
    https://mail.python.org/pipermail/tutor/2003-December/027032.html
    """

    # Example grammar with normal operator precedence:
    # expression ::=  factor
    #               | factor '+' factor
    # factor     ::=  term
    #               | term '*' term
    # term       ::= NUMBER
    #               | '(' expression ')'

    def __init__(self, tokens):
        self.tokens = tokens

    @classmethod
    def from_string(cls, s):
        """Tokenize/lex a string and return an instance"""
        return cls(s.replace("(", " ( ").replace(")", " ) ").split() + ["EOF"])

    def peek_token(self):
        """Looks at the next token in our token stream."""
        return self.tokens[0]

    def consume_token(self):
        """Pops off the next token in our token stream."""
        next_token = self.tokens[0]
        del self.tokens[0]
        return next_token

    def parse_expression(self):
        """Returns a parsed expression.  An expression may consist of a
        bunch of chained factors."""
        expression = self.parse_factor()
        while True:
            if self.peek_token() in (PLUS):
                operation = self.consume_token()
                factor = self.parse_factor()
                expression = [operation, expression, factor]
            else:
                break
        return expression

    def parse_factor(self):
        """Returns a parsed factor.   A factor may consist of a bunch of
        chained terms."""
        factor = self.parse_term()
        while True:
            if self.peek_token() in (TIMES):
                operation = self.consume_token()
                term = self.parse_term()
                factor = [operation, factor, term]
            else:
                break
        return factor

    def parse_term(self):
        """Returns a parsed term.  A term may consist of a number, or a
        parenthesized expression."""
        if self.peek_token() != LPAREN:
            return int(self.consume_token())
        else:
            self.consume_token()  # eat up the lparen
            expression = self.parse_expression()
            self.consume_token()  # eat up the rparen
            return expression


class ArithmeticParserPart1(ArithmeticParser):
    """ `+` and `*` have the same precedence"""

    def parse_expression(self):
        """Returns a parsed expression.  An expression may consist of a
        bunch of chained terms."""
        expression = self.parse_term()
        while True:
            if self.peek_token() in (PLUS, TIMES):
                operation = self.consume_token()
                factor = self.parse_term()
                expression = [operation, expression, factor]
            else:
                break
        return expression


class ArithmeticParserPart2(ArithmeticParser):
    """ `+` has higher precedence than `*`"""

    def parse_expression(self):
        """Returns a parsed expression.  An expression may consist of a
        bunch of chained factors."""
        expression = self.parse_factor()
        while True:
            if self.peek_token() in (TIMES):
                operation = self.consume_token()
                factor = self.parse_factor()
                expression = [operation, expression, factor]
            else:
                break
        return expression

    def parse_factor(self):
        """Returns a parsed factor.   A factor may consist of a bunch of
        chained terms."""
        factor = self.parse_term()
        while True:
            if self.peek_token() in (PLUS):
                operation = self.consume_token()
                term = self.parse_term()
                factor = [operation, factor, term]
            else:
                break
        return factor


def eval_ast(ast):
    if isinstance(ast, list):
        op, first, second = ast
        first_val = eval_ast(first)
        second_val = eval_ast(second)
        if op == PLUS:
            return first_val + second_val
        elif op == TIMES:
            return first_val * second_val
        raise ValueError(f"Unknown operator {op}")
    else:
        return ast


def solve_1(s: str) -> int:
    ast = ArithmeticParserPart1.from_string(s).parse_expression()
    return eval_ast(ast)


def solve_2(s: str) -> int:
    ast = ArithmeticParserPart2.from_string(s).parse_expression()
    return eval_ast(ast)


assert eval_ast(ArithmeticParser.from_string("2 + 2 * 2").parse_expression()) == 6
assert solve_1("1 + 2 * 3 + 4 * 5 + 6") == 71
assert solve_1("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert solve_1("2 * 3 + (4 * 5)") == 26
assert solve_1("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
assert solve_1("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
assert solve_1("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632

assert solve_2("1 + 2 * 3 + 4 * 5 + 6") == 231
assert solve_2("1 + (2 * 3) + (4 * (5 + 6))") == 51
assert solve_2("2 * 3 + (4 * 5)") == 46
assert solve_2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
assert solve_2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
assert solve_2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340

lines = open("d18/input.txt").read().splitlines()
print(sum(solve_1(l) for l in lines))
print(sum(solve_2(l) for l in lines))
