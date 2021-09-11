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
class Function(Stmt):
    name: Token
    params: list
    body: list


@dataclass
class If(Stmt):
    condition: Expr
    thenBranch: Stmt
    elseBranch: Stmt


@dataclass
class Print(Stmt):
    expression: Expr


@dataclass
class Return(Stmt):
    keyword: Token
    value: Expr


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr


@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt
