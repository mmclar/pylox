from classes import LoxClass, LoxInstance, INIT_METHOD_NAME
from environment import Environment, LoxRuntimeError
from expressions import Binary, Grouping, Literal, Unary, Variable, Assign, Logical, Call, Expr, Get, Set, This
from functions import Clock, LoxFunction, ReturnException
from statements import Print, Expression, Var, Block, If, While, Function, Return, Class
from stmtvisitor import StmtVisitor
from tokens import TokenType, Token
from exprvisitor import ExprVisitor
from util import Errors


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment(None)
        self.environment = self.globals
        self.locals = {}

        self.globals.define('clock', Clock())

    def interpret(self, statements):
        result = None
        try:
            for statement in statements:
                result = self.execute(statement)
        except LoxRuntimeError as ex:
            Errors.error(ex.message, ex.token)
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
        finally:
            self.environment = previous

    def resolve(self, expr: Expr, depth):
        self.locals[expr] = depth

    # Implement ExprVisitor
    def visitAssignExpr(self, expr: Assign):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assignAt(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

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

    def visitCallExpr(self, expr: Call):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(argument) for argument in expr.arguments]
        try:
            if len(arguments) != callee.arity():
                raise Exception(f'Expected {callee.arity()} arguments but got {len(arguments)}.')
            return callee.call(self, arguments)
        except AttributeError:
            raise Exception('Can only call functions and classes.')

    def visitGetExpr(self, expr: Get):
        obj = self.evaluate(expr.object)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)
        raise LoxRuntimeError(expr.name, 'Only instances may have properties.')

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

    def visitSetExpr(self, expr: Set):
        obj = self.evaluate(expr.object)
        if not isinstance(obj, LoxInstance):
            raise LoxRuntimeError(expr.name, 'Only instances have fields.')
        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visitThisExpr(self, expr: This):
        return self.lookupVariable(expr.keyword, expr)

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            return -float(right)
        if expr.operator.type == TokenType.BANG:
            return not right

    def visitVariableExpr(self, expr: Variable):
        return self.lookupVariable(expr.name, expr)

    def lookupVariable(self, name: Token, expr: Expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.getAt(distance, name.lexeme)
        return self.globals.get(name)

    # Implement StmtVisitor
    def visitBlockStmt(self, stmt: Block):
        self.executeBlock(stmt.statements, Environment(self.environment))

    def visitClassStmt(self, stmt: Class):
        self.environment.define(stmt.name.lexeme, None)
        methods = {}
        for method in stmt.methods:
            function = LoxFunction(method, self.environment, method.name.lexeme == INIT_METHOD_NAME)
            methods[method.name.lexeme] = function
        cls = LoxClass(stmt.name.lexeme, methods)
        self.environment.assign(stmt.name, cls)

    def visitExpressionStmt(self, stmt: Expression):
        return self.evaluate(stmt.expression)  # Return evaluated expression for tests

    def visitFunctionStmt(self, stmt: Function):
        function = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)

    def visitIfStmt(self, stmt: If):
        if self.evaluate(stmt.condition):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch:
            self.execute(stmt.elseBranch)

    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(value)

    def visitReturnStmt(self, stmt: Return):
        value = stmt.value and self.evaluate(stmt.value)
        e = ReturnException(value)
        raise e

    def visitVarStmt(self, stmt: Var):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visitWhileStmt(self, stmt: While):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body)
