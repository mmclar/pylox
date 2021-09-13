from enum import Enum, auto

from environment import LoxRuntimeError
from tokens import Token

INIT_METHOD_NAME = 'init'


class ClassType(Enum):
    NONE = auto()
    CLASS = auto


class LoxClass:
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def __str__(self):
        return f'{self.name}'

    def findMethod(self, name):
        return self.methods.get(name) or (
            self.superclass and self.superclass.findMethod(name)
        )

    def call(self, interpreter, arguments):
        instance = LoxInstance(self)
        if initializer := self.findMethod(INIT_METHOD_NAME):
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self):
        if initializer := self.findMethod(INIT_METHOD_NAME):
            return initializer.arity()
        return 0


class LoxInstance:
    def __init__(self, cls: LoxClass):
        self.cls = cls
        self.fields = {}

    def __str__(self):
        return f'{self.cls} instance'

    def get(self, name: Token):
        try:
            if method := self.cls.findMethod(name.lexeme):
                return method.bind(self)
            return self.fields[name.lexeme]
        except KeyError:
            raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'")

    def set(self, name: Token, value):
        self.fields[name.lexeme] = value
