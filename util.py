import sys

from tokens import TokenType


class Errors:
    hadError = False

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def error(message, line=None, token=None):
        if (line is None) == (token is None):
            raise ValueError('Need exactly one of `line` or `token`.')
        if line:
            Errors.report(line, '', message)
        else:
            where = ' at end' if token.type == TokenType.EOF else f'at "{token.lexeme}"'
            Errors.report(message, token.line, where)

    @staticmethod
    def report(message, line, where):
        Errors.eprint(f'[line {line}] Error {where}: {message}')
        Errors.hadError = True
