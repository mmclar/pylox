from dataclasses import dataclass

from expressions import Expr
from tokens import Token


class Stmt:
    def accept(self, visitor):
        return getattr(visitor, f'visit{type(self).__name__}Stmt')(self)


@dataclass
class Block(Stmt):
    statements: list


@dataclass
class Expression(Stmt):
    expression: Expr


@dataclass
class Print(Stmt):
    expression: Expr


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr
