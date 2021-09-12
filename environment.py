from dataclasses import dataclass

from tokens import Token
from util import Errors


@dataclass
class LoxRuntimeError(Exception):
    token: Token
    message: str


class Environment:
    def __init__(self, enclosing):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def ancestor(self, distance):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment

    def getAt(self, distance, name):
        return self.ancestor(distance).values.get(name)

    def assignAt(self, distance, name: Token, value):
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing:
            self.enclosing.assign(name, value)
        else:
            raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
