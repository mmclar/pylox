from expressions import Binary, Unary, Literal, Grouping
from tokens import TokenType
from util import Errors


class Parser:
    class ParseError(Exception):
        pass

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except Parser.ParseError:
            return None

    # Grammar rules
    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ) after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), 'Expect expression.')

    # Helper methods
    def match(self, *tokenTypes):
        for tokenType in tokenTypes:
            if self.check(tokenType):
                self.advance()
                return True
        return False

    def check(self, tokenType):
        return False if self.isAtEnd() else self.peek().type == tokenType

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, tokenType, message):
        if self.check(tokenType):
            return self.advance()
        raise self.error(self.peek(), message)

    @staticmethod
    def error(token, message):
        Errors.error(message, token=token)
        return Parser.ParseError()

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return

        if self.peek().type in [
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN,
        ]:
            return

        self.advance()
