import abc

from statements import Expression, Print


class StmtVisitor(abc.ABC):
    @abc.abstractmethod
    def visitExpressionStmt(self, stmt: Expression):
        pass

    @abc.abstractmethod
    def visitPrintStmt(self, stmt: Print):
        pass
