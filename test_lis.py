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


def test_lambda_procedure():
    program = '(begin (define circle-area (lambda (r) (* pi (* r r)))) (circle-area 10))'
    assert eval(parse(program)) == 314.1592653589793
