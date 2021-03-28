from dataclasses import dataclass

from expressions import Expr


class Stmt:
    def accept(self, visitor):
        return getattr(visitor, f'visit{type(self).__name__}Stmt')(self)


@dataclass
class Expression(Stmt):
    expression: Expr


@dataclass
class Print(Stmt):
    expression: Expr
