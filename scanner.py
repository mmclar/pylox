import string

from tokens import Token, TokenType
from util import Errors


class Scanner:

    def __init__(self, source):
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.source = source

    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        c = self.advance()

        def _handleSlash(slf):
            if slf.match('/'):
                while slf.peek() != '\n' and not self.isAtEnd():
                    self.advance()
                return None
            else:
                return TokenType.SLASH

        def _handleNewline(slf):
            slf.line += 1
            return None

        def _handleString(slf):
            while slf.peek() != '"' and not slf.isAtEnd():
                if slf.peek() == '\n':
                    slf.line += 1
                slf.advance()

            if slf.isAtEnd():
                Errors.error(slf.line, 'Unterminated string.')
                return None

            # Handle closing '"'
            slf.advance()

            # Trim the surrounding quotes
            value = slf.source[slf.start + 1:slf.current - 1]
            return TokenType.STRING, value

        def _handleNumber(slf):
            while isDigit(slf.peek()):
                slf.advance()

            if slf.peek() == '.' and isDigit(slf.peekNext()):
                slf.advance()
                while isDigit(slf.peek()):
                    slf.advance()
            text = slf.source[slf.start:slf.current]
            return TokenType.NUMBER, float(text)

        def _handleIdentifier(slf):

            while isAlphaNumeric(slf.peek()):
                slf.advance()

            text = slf.source[slf.start:slf.current]

            tokenType = {
                'and': TokenType.AND,
                'class': TokenType.CLASS,
                'else': TokenType.ELSE,
                'false': TokenType.FALSE,
                'for': TokenType.FOR,
                'fun': TokenType.FUN,
                'if': TokenType.IF,
                'nil': TokenType.NIL,
                'or': TokenType.OR,
                'print': TokenType.PRINT,
                'return': TokenType.RETURN,
                'super': TokenType.SUPER,
                'this': TokenType.THIS,
                'true': TokenType.TRUE,
                'var': TokenType.VAR,
                'while': TokenType.WHILE,
            }.get(text, TokenType.IDENTIFIER)

            return tokenType, text if tokenType == TokenType.IDENTIFIER else None

        tokenMap = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ',': TokenType.COMMA,
            '-.': TokenType.MINUS,
            '+': TokenType.PLUS,
            ';': TokenType.SEMICOLON,
            '*': TokenType.STAR,
            '!': lambda slf: TokenType.BANG_EQUAL if slf.match('=') else TokenType.BANG,
            '=': lambda slf: TokenType.EQUAL_EQUAL if slf.match('=') else TokenType.EQUAL,
            '<': lambda slf: TokenType.LESS_EQUAL if slf.match('=') else TokenType.LESS,
            '>': lambda slf: TokenType.GREATER_EQUAL if slf.match('=') else TokenType.GREATER,
            '/': _handleSlash,
            ' ': None,
            '\r': None,
            '\t': None,
            '\n': _handleNewline,
            '"': _handleString,
        }
        for d in string.digits:
            tokenMap[str(d)] = _handleNumber
        for a in string.ascii_letters:
            tokenMap[a] = _handleIdentifier

        token = tokenMap[c]

        if callable(token):
            token = token(self)
        if token is not None:
            if type(token) is TokenType:  # better way to check if we got one value and make the second None?
                token = (token, None)
            self.addToken(*token)

    def match(self, expected):
        if self.isAtEnd() or self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return None
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return None
        return self.source[self.current + 1]

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def addToken(self, tokenType, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tokenType, text, literal, self.line))


def isDigit(c):
    return c is not None and c in string.digits


def isAlpha(c):
    return c is not None and c in string.ascii_letters + string.digits


def isAlphaNumeric(c):
    return isAlpha(c) or isDigit(c)
