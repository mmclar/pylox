from scanner import Scanner


def testLexer():
    cases = [
        ('1', '[(TokenType.NUMBER, 1.0), (TokenType.EOF, None)]'),
        ('"A"', '[(TokenType.STRING, A), (TokenType.EOF, None)]'),
        ('3.14159', '[(TokenType.NUMBER, 3.14159), (TokenType.EOF, None)]'),
        ('3.14159 // Comment time', '[(TokenType.NUMBER, 3.14159), (TokenType.EOF, None)]'),
        ('someVar', '[(TokenType.IDENTIFIER, someVar), (TokenType.EOF, None)]'),
        ('for', '[(TokenType.FOR, None), (TokenType.EOF, None)]'),
        ('while', '[(TokenType.WHILE, None), (TokenType.EOF, None)]'),
    ]

    passed = 0
    for source, expectedStr in cases:
        actual = Scanner(source).scanTokens()
        print(f'Testing source:\n{source}')
        if expectedStr != str(actual):
            print(f'Failed.\nExpected:\n{expectedStr}\n\nActual:\n{actual}\n')
        else:
            passed += 1
            print('Passed.\n')
    print(f'{passed}/{len(cases)} passed.')


if __name__ == '__main__':
    testLexer()
