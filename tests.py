from astprinter import Binary, Literal, Grouping, Unary, AstPrinter
from lox import Lox
from scanner import Scanner
from tokens import Token, TokenType


lexerCases = [
    ('1', '[(TokenType.NUMBER, 1.0), (TokenType.EOF, None)]'),
    ('"A"', '[(TokenType.STRING, A), (TokenType.EOF, None)]'),
    ('3.14159', '[(TokenType.NUMBER, 3.14159), (TokenType.EOF, None)]'),
    ('3.14159 // Comment time', '[(TokenType.NUMBER, 3.14159), (TokenType.EOF, None)]'),
    ('someVar', '[(TokenType.IDENTIFIER, someVar), (TokenType.EOF, None)]'),
    ('for', '[(TokenType.FOR, None), (TokenType.EOF, None)]'),
    ('while', '[(TokenType.WHILE, None), (TokenType.EOF, None)]'),
]


astCases = [
    (Binary(
        left=Literal(value=1),
        operator=Token(TokenType.PLUS, '+', None, 1),
        right=Literal(value=2),
    ), '(+ 1 2)'),
    (Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.6)
        )
    ), '(* (- 123) (group 45.6))'),
]


parserCases = [
    ('1', '1.0'),
    ('true', 'True'),
    ('-1', '-1.0'),
    ('(1)', '1.0'),
    ('!true', 'False'),
    ('!!true', 'True'),
    ('!!0', 'False'),
    ('!!1', 'True'),
    ('1==1', 'True'),
    ('1<2', 'True'),
    ('1>2', 'False'),
    ('2>=2', 'True'),
    ('2<=2', 'True'),
]


def test(cases, testFn):
    passed = 0
    for testVal, expectedStr in cases:
        actual = testFn(testVal)
        print(f'Testing input:\n{testVal}')
        if expectedStr != str(actual):
            print(f'Failed.\nExpected:\n{expectedStr}\nActual:\n{actual}\n')
        else:
            passed += 1
            print('Passed.\n')
    print(f'{passed}/{len(cases)} passed.')


if __name__ == '__main__':
    test(lexerCases, lambda source: Scanner(source).scanTokens())
    test(astCases, lambda expr: AstPrinter().print(expr))
    test(parserCases, lambda source: Lox.interpretSource(source))
