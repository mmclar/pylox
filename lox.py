import sys

from astprinter import AstPrinter
from interpreter import Interpreter
from parser import Parser
from scanner import Scanner
from util import Errors


class Lox:
    def main(self, args):
        if len(args) > 2:
            print('Usage: pylox [script]')
            sys.exit(64)
        elif len(args) == 2:
            # self.runFile(args[1])
            pass
        else:
            self.runPrompt()

    def runPrompt(self):
        print('Welcome to lox')
        while True:
            print('lox> ', end='')
            try:
                line = input()
                if line is None:
                    break
                self.run(line)
            except EOFError:
                print('\nExiting lox')
                break

    @staticmethod
    def interpretSource(source):
        tokens = Scanner(source).scanTokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if Errors.hadError:
            return

        return Interpreter().interpret(expression)

    @staticmethod
    def run(source):
        Lox.interpretSource(source)


if __name__ == '__main__':
    Lox().main(sys.argv)
