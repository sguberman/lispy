def tokenize(chars):
    """
    Convert a string of characters into a list of tokens.
    """
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    """
    Read a Scheme expression from a string.
    """
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens):
    """
    Read an expression from a sequence of tokens.
    """
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token):
    """
    Numbers become numbers; every other token is a symbol.
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


Symbol = str            # A Scheme Symbol is implemented as a Python str
List = list             # A Scheme List is implemented as a Python list
Number = (int, float)   # A Scheme Number is implemented as a Python int or float
Env = dict              # An environment is a mapping of {variable: value}


def standard_env():
    """
    An environment with some Scheme standard procedures.
    """
    import math
    import operator as op
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.truediv,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': lambda *x: x[0](*x[1:]),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x,y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


global_env = standard_env()


def eval(x, env=global_env):
    """
    Evaluate an expression in an environment.
    """
    if isinstance(x, Symbol):       # variable reference
        return env[x]
    elif not isinstance(x, List):   # constant literal
        return x
    elif x[0] == 'quote':           # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':              # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':          # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    else:
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)
