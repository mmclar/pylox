from dataclasses import dataclass

from tokens import Token


class Expr:
    def accept(self, visitor):
        return getattr(visitor, f'visit{type(self).__name__}Expr')(self)


@dataclass
class Binary(Expr):
    left: 'Expr'
    operator: Token
    right: 'Expr'


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Literal(Expr):
    value: object


@dataclass
class Unary(Expr):
    operator: Token
    right: 'Expr'
