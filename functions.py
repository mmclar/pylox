import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from classes import LoxInstance, INIT_METHOD_NAME
from environment import Environment
from statements import Function


@dataclass
class ReturnException(Exception):
    value: Any


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()


class LoxFunction:
    def __init__(self, declaration: Function, closure: Environment, isInitializer):
        self.isInitializer = isInitializer
        self.closure = closure
        self.declaration = declaration

    def bind(self, instance: LoxInstance):
        environment = Environment(self.closure)
        environment.define('this', instance)
        return LoxFunction(self.declaration, environment, self.isInitializer)

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for param, argument in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, argument)
        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnException as returnValue:
            return self.closure.getAt(0, INIT_METHOD_NAME) if self.isInitializer else returnValue.value
        if self.isInitializer:
            return self.closure.getAt(0, INIT_METHOD_NAME)


class Clock:
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return datetime.datetime.now().timestamp()
