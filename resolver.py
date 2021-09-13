from typing import Union

from classes import ClassType, INIT_METHOD_NAME
from expressions import Unary, Literal, Grouping, Binary, Expr, Variable, Logical, Call, Assign, Get, Set, This
from exprvisitor import ExprVisitor
from functions import FunctionType
from interpreter import Interpreter
from statements import Block, Print, Expression, Stmt, While, Var, Return, If, Function, Class
from stmtvisitor import StmtVisitor
from tokens import Token
from util import Errors


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.currentFunctionType = FunctionType.NONE
        self.currentClassType = ClassType.NONE

    def resolveStatements(self, statements):
        for statement in statements:
            self.resolve(statement)

    def resolve(self, stmtExpr: Union[Expr, Stmt]):
        stmtExpr.accept(self)

    def resolveFunction(self, function: Function, type: FunctionType):
        enclosingFunctionType = self.currentFunctionType
        self.currentFunctionType = type

        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolveStatements(function.body)
        self.endScope()

        self.currentFunctionType = enclosingFunctionType

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if name.lexeme in self.curScope:
            Errors.error("Already a variable with this name in this scope.", name)
        self.curScope[name.lexeme] = False

    def define(self, name: Token):
        self.curScope[name.lexeme] = True

    def resolveLocal(self, expr: Expr, name: Token):
        i = len(self.scopes) - 1
        while i >= 0:
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
            i -= 1

    @property
    def curScope(self):
        return self.scopes[-1] if self.scopes else {}

    # Implement ExprVisitor
    def visitAssignExpr(self, expr: Assign):
        self.resolve(expr.value)
        self.resolveLocal(expr, expr.name)

    def visitBinaryExpr(self, expr: Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitCallExpr(self, expr: Call):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visitGetExpr(self, expr: Get):
        self.resolve(expr.object)

    def visitGroupingExpr(self, expr: Grouping):
        self.resolve(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        pass

    def visitLogicalExpr(self, expr: Logical):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitSetExpr(self, expr: Set):
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visitThisExpr(self, expr: This):
        if self.currentClassType == ClassType.NONE:
            Errors.error("Can't use 'this' outside of a class.", expr.keyword)
        self.resolveLocal(expr, expr.keyword)

    def visitUnaryExpr(self, expr: Unary):
        self.resolve(expr.right)

    def visitVariableExpr(self, expr: Variable):
        if self.scopes and self.curScope.get(expr.name.lexeme) is False:
            Errors.error("Can't read local variable in its own initializer.", expr.name)
        self.resolveLocal(expr, expr.name)

    # Implement StmtVisitor
    def visitBlockStmt(self, stmt: Block):
        self.beginScope()
        self.resolveStatements(stmt.statements)
        self.endScope()

    def visitClassStmt(self, stmt: Class):
        enclosingClassType = self.currentClassType
        self.currentClassType = ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                Errors.error("A class can't inherit from itself.", stmt.superclass.name)
            self.resolve(stmt.superclass)

        self.beginScope()
        self.curScope['this'] = True
        for method in stmt.methods:
            declarationFunctionType = (
                FunctionType.INITIALIZER
                if method.name.lexeme == INIT_METHOD_NAME
                else FunctionType.METHOD
            )
            self.resolveFunction(method, declarationFunctionType)
        self.endScope()

        self.currentClassType = enclosingClassType

    def visitExpressionStmt(self, stmt: Expression):
        self.resolve(stmt.expression)

    def visitFunctionStmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt, FunctionType.FUNCTION)

    def visitIfStmt(self, stmt: If):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch:
            self.resolve(stmt.elseBranch)

    def visitPrintStmt(self, stmt: Print):
        self.resolve(stmt.expression)

    def visitReturnStmt(self, stmt: Return):
        if self.currentFunctionType == FunctionType.NONE:
            Errors.error("Can't return from top-level code.", stmt.keyword)
        if stmt.value:
            if self.currentFunctionType == FunctionType.INITIALIZER:
                Errors.error("Can't return a value from an initializer.", stmt.keyword)
            self.resolve(stmt.value)

    def visitVarStmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initializer:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visitWhileStmt(self, stmt: While):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
