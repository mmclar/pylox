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


class AstPrinter:
    def print(self, expr: Expr):
        return expr.accept(self)

    def parenthesize(self, name, *exprs):
        inner = ''.join(f' {expr.accept(self)}' for expr in exprs)
        return f'({name}{inner})'

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        return str(expr.value) if expr.value is not None else 'nil'

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)
