from expressions import Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Expr, Call
from statements import Print, Expression, Var, Block, If, While, Function, Return
from tokens import TokenType
from util import Errors

MAX_ARITY = 255


class Parser:
    class ParseError(Exception):
        pass

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements

    # Grammar rules
    def statement(self):
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.RETURN):
            return self.returnStatement();
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expressionStatement()

    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = (
            None if self.match(TokenType.SEMICOLON)
            else self.varDeclaration() if self.match(TokenType.VAR)
            else self.expressionStatement()
        )
        condition = (
            Literal(True) if self.match(TokenType.SEMICOLON)
            else self.expression()
        )
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        increment = (
            None if self.check(TokenType.RIGHT_PAREN)
            else self.expression()
        )
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        if increment:
            body = Block([body, increment])
        body = While(condition, body)
        if initializer:
            body = Block([initializer, body])
        return body

    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch = self.statement()
        elseBranch = self.statement() if self.match(TokenType.ELSE) else None
        return If(condition, thenBranch, elseBranch)

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def returnStatement(self):
        keyword = self.previous()
        value = self.expression() if not self.check(TokenType.SEMICOLON) else None
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword, value)

    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, 'Expect variable name.')
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return While(condition, body)

    def expressionStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(value)

    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, f'Expect {kind} name.')
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) > MAX_ARITY:
                    self.error(self.peek(), f"Can't have more than {MAX_ARITY} parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, 'Expect parameter name.'))
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()
        return Function(name, parameters, body)

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def assignment(self):
        expr = self.orr()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            Errors.error("Invalid assignment target.", equals)

        return expr

    def orr(self):
        expr = self.andd()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.andd()
            expr = Logical(expr, operator, right)
        return expr

    def andd(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except:  # really want to catch ParseError here
            self.synchronize()

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.call()

    def finishCall(self, callee: Expr):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) > MAX_ARITY:
                    self.error(self.peek(), f"Can't have more than {MAX_ARITY} arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Call(callee, paren, arguments)

    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            else:
                break
        return expr

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ) after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), 'Expect expression.')

    # Helper methods
    def match(self, *tokenTypes):
        for tokenType in tokenTypes:
            if self.check(tokenType):
                self.advance()
                return True
        return False

    def check(self, tokenType):
        return False if self.isAtEnd() else self.peek().type == tokenType

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, tokenType, message):
        if self.check(tokenType):
            return self.advance()
        raise self.error(self.peek(), message)

    @staticmethod
    def error(token, message):
        Errors.error(message, token)
        return Parser.ParseError()

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()
