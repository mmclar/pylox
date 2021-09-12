import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from environment import Environment
from statements import Function


@dataclass
class ReturnException(Exception):
    value: Any


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class LoxFunction:
    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for param, argument in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, argument)
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnException as returnValue:
            return returnValue.value


class Clock:
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return datetime.datetime.now().timestamp()
