import abc

from expressions import Binary, Grouping, Literal, Unary


class ExprVisitor(abc.ABC):
    @abc.abstractmethod
    def visitBinaryExpr(self, expr: Binary):
        pass

    @abc.abstractmethod
    def visitGroupingExpr(self, expr: Grouping):
        pass

    @abc.abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        pass

    @abc.abstractmethod
    def visitUnaryExpr(self, expr: Unary):
        pass
