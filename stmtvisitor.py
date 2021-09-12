import abc

from statements import Expression, Print, Block, Function, If, Return, Var, While


class StmtVisitor(abc.ABC):
    @abc.abstractmethod
    def visitBlockStmt(self, stmt: Block):
        pass

    @abc.abstractmethod
    def visitExpressionStmt(self, stmt: Expression):
        pass

    @abc.abstractmethod
    def visitFunctionStmt(self, stmt: Function):
        pass

    @abc.abstractmethod
    def visitIfStmt(self, stmt: If):
        pass

    @abc.abstractmethod
    def visitPrintStmt(self, stmt: Print):
        pass

    @abc.abstractmethod
    def visitReturnStmt(self, stmt: Return):
        pass

    @abc.abstractmethod
    def visitVarStmt(self, stmt: Var):
        pass

    @abc.abstractmethod
    def visitWhileStmt(self, stmt: While):
        pass
