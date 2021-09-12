from environment import LoxRuntimeError
from tokens import Token


class LoxClass:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def call(self, interpreter, arguments):
        return LoxInstance(self)

    def arity(self):
        return 0


class LoxInstance:
    def __init__(self, cls: LoxClass):
        self.cls = cls
        self.fields = {}

    def __str__(self):
        return f'{self.cls} instance'

    def get(self, name: Token):
        try:
            return self.fields[name.lexeme]
        except KeyError:
            raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'")

    def set(self, name: Token, value):
        self.fields[name.lexeme] = value
