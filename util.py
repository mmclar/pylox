import sys

from tokens import TokenType, Token


class Errors:
    hadError = False

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def error(message, token: Token):
        Errors.hadError = True
        if token:
            where = ' end' if token.type == TokenType.EOF else f'"{token.lexeme}"'
            line = token.line
            Errors.eprint(f'[line {line} at {where}] Error: {message}')
        else:
            raise ValueError('Need at least one of `line` or `token`.')
