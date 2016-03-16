from lis import *


program = '(begin (define r 10) (* pi (* r r)))'

def test_tokenize():
    result = ['(', 'begin', '(', 'define', 'r', '10', ')', '(', '*', 'pi', '(', '*', 'r', 'r', ')', ')', ')']
    assert tokenize(program) == result


def test_parse():
    result = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
    assert parse(program) == result


def test_eval():
    assert eval(parse(program)) == 314.1592653589793
