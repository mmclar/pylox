from dataclasses import dataclass

from tokens import Token


class Expr:
    def accept(self, visitor):
        return getattr(visitor, f'visit{type(self).__name__}Expr')(self)


@dataclass(unsafe_hash=True)
class Assign(Expr):
    name: Token
    value: Expr


@dataclass(unsafe_hash=True)
class Binary(Expr):
    left: 'Expr'
    operator: Token
    right: 'Expr'


@dataclass(unsafe_hash=True)
class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list


@dataclass(unsafe_hash=True)
class Get(Expr):
    object: Expr
    name: Token


@dataclass(unsafe_hash=True)
class Grouping(Expr):
    expression: Expr


@dataclass(unsafe_hash=True)
class Literal(Expr):
    value: object


@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass(unsafe_hash=True)
class Set(Expr):
    object: Expr
    name: Token
    value: Expr


@dataclass(unsafe_hash=True)
class Super(Expr):
    keyword: Token
    method: Token


@dataclass(unsafe_hash=True)
class This(Expr):
    keyword: Token


@dataclass
class Unary(Expr):
    operator: Token
    right: 'Expr'


@dataclass(unsafe_hash=True)
class Variable(Expr):
    name: Token
