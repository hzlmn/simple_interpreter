import itertools
import sys
from collections import deque


class Node:
    def __repr__(self):
        identifier = type(self).__name__
        return f"<{identifier} {self.value}>"


class ExprNode(Node):
    def __init__(self, value):
        self.value = value


class SetNode(Node):
    def __init__(self, file):
        with open(file) as fp:
            self.value = set(fp.read().split())


def SUM(*sets):
    return list(sorted(set(itertools.chain.from_iterable(sets))))


def DIF(*sets):
    first, *rest = sets

    return list(sorted(first.difference(SUM(*rest))))


def INT(*sets):
    return list(sorted(set.intersection(*sets)))


def builtins():
    env = {
        "SUM": SUM,
        "DIF": DIF,
        "INT": INT,
    }
    return env


def parse(tokens):
    return parse_expr(tokens)


def parse_expr(tokens):
    if not tokens:
        raise SyntaxError

    token = tokens.popleft()
    if "[" == token:
        exprs = []
        while tokens[0] != "]":
            exprs.append(parse_expr(tokens))
        tokens.popleft()
        return exprs
    elif "]" == token:
        raise SyntaxError(f"Unexpected token:{token}")
    else:
        return get_node(token)


def get_node(token):
    if token.endswith(".txt"):
        return SetNode(token)

    return ExprNode(token)


def evaluate(ast, env=builtins()):
    if isinstance(ast, ExprNode):
        return env.get(ast.value)

    if isinstance(ast, SetNode):
        return ast.value

    proc = evaluate(ast[0], env)
    args = [evaluate(exp, env) for exp in ast[1:]]

    return proc(*args)


def show_result(result):
    assert isinstance(result, list)

    data = "\n".join(result)

    sys.stdout.write(data)


if __name__ == "__main__":
    _, *tokens = sys.argv

    ast = parse(deque(tokens))

    result = evaluate(ast)

    show_result(result)
