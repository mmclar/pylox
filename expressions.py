from dataclasses import dataclass

from tokens import Token


class Expr:
    def accept(self, visitor):
        return getattr(visitor, f'visit{type(self).__name__}Expr')(self)


@dataclass
class Assign(Expr):
    name: Token
    value: Expr


@dataclass
class Binary(Expr):
    left: 'Expr'
    operator: Token
    right: 'Expr'


@dataclass
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass
class Literal(Expr):
    value: object


@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Unary(Expr):
    operator: Token
    right: 'Expr'


@dataclass
class Variable(Expr):
    name: Token
