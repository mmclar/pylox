from environment import Environment
from expressions import Binary, Grouping, Literal, Unary, Variable, Assign, Logical
from statements import Print, Expression, Var, Block, If, While
from stmtvisitor import StmtVisitor
from tokens import TokenType
from exprvisitor import ExprVisitor
from util import Errors


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.environment = Environment(None)

    def interpret(self, statements):
        result = None
        try:
            for statement in statements:
                result = self.execute(statement)
        except RuntimeError:
            raise
        return result  # Return the result, for tests

    def evaluate(self, expression):
        return expression.accept(self)

    def execute(self, stmt):
        return stmt.accept(self)

    def executeBlock(self, statements, environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        except:
            Errors.error(statements)
        self.environment = previous

    # Implement ExprVisitor
    def visitBlockStmt(self, stmt: Block):
        self.executeBlock(stmt.statements, Environment(self.environment))

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            return left - right
        if expr.operator.type == TokenType.PLUS:
            return left + right
        if expr.operator.type == TokenType.SLASH:
            return left / right
        if expr.operator.type == TokenType.STAR:
            return left + right
        if expr.operator.type == TokenType.GREATER:
            return left > right
        if expr.operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        if expr.operator.type == TokenType.LESS:
            return left < right
        if expr.operator.type == TokenType.LESS_EQUAL:
            return left <= right
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return left == right

    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitLogicalExpr(self, expr: Logical):
        left = self.evaluate(expr.left)

        # Don't evaluate right if left side of OR is true or if left side of AND is false.
        if expr.operator.type == TokenType.OR:
            if left:
                return left
        else:
            if not left:
                return left

        return self.evaluate(expr.right)

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -float(right)
        if expr.operator.type == TokenType.BANG:
            return not right

    def visitVariableExpr(self, expr: Variable):
        return self.environment.get(expr.name)

    # Implement StmtVisitor
    def visitExpressionStmt(self, stmt: Expression):
        return self.evaluate(stmt.expression)  # Return evaluated expression for tests

    def visitIfStmt(self, stmt: If):
        if self.evaluate(stmt.condition):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch:
            self.execute(stmt.elseBranch)

    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(value)

    def visitVarStmt(self, stmt: Var):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visitWhileStmt(self, stmt: While):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body)

    def visitAssignExpr(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

