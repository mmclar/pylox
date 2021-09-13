import abc

from expressions import Binary, Grouping, Literal, Unary, Assign, Call, Logical, Variable, Get, Set, This, Super


class ExprVisitor(abc.ABC):
    @abc.abstractmethod
    def visitAssignExpr(self, expr: Assign):
        pass

    @abc.abstractmethod
    def visitBinaryExpr(self, expr: Binary):
        pass

    @abc.abstractmethod
    def visitCallExpr(self, expr: Call):
        pass

    @abc.abstractmethod
    def visitGetExpr(self, expr: Get):
        pass

    @abc.abstractmethod
    def visitGroupingExpr(self, expr: Grouping):
        pass

    @abc.abstractmethod
    def visitLiteralExpr(self, expr: Literal):
        pass

    @abc.abstractmethod
    def visitLogicalExpr(self, expr: Logical):
        pass

    @abc.abstractmethod
    def visitSetExpr(self, expr: Set):
        pass

    @abc.abstractmethod
    def visitSuperExpr(self,expr: Super):
        pass

    @abc.abstractmethod
    def visitThisExpr(self, expr: This):
        pass

    @abc.abstractmethod
    def visitUnaryExpr(self, expr: Unary):
        pass

    @abc.abstractmethod
    def visitVariableExpr(self, expr: Variable):
        pass
