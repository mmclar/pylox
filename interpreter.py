from expressions import Binary, Grouping, Literal, Unary
from statements import Print, Expression
from stmtvisitor import StmtVisitor
from tokens import TokenType
from exprvisitor import ExprVisitor


class Interpreter(ExprVisitor, StmtVisitor):
    def interpret(self, statements):
        result = None
        try:
            for statement in statements:
                result = self.execute(statement)
        except RuntimeError:
            raise
        return result

    def evaluate(self, expression):
        return expression.accept(self)

    def execute(self, stmt):
        return stmt.accept(self)

    # Implement ExprVisitor
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

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -float(right)
        if expr.operator.type == TokenType.BANG:
            return not right

    # Implement StmtVisitor
    def visitExpressionStmt(self, stmt: Expression):
        return self.evaluate(stmt.expression)

    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(value)

