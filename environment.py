from tokens import Token
from util import Errors


class Environment:
    def __init__(self, enclosing):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        Errors.error(f"Undefined variable '{name.lexeme}'.", name)

    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing:
            self.enclosing.assign(name, value)
        else:
            Errors.error(f"Undefined variable '{name.lexeme}'.", name)

