import sys

from astprinter import AstPrinter
from interpreter import Interpreter
from parser import Parser
from scanner import Scanner
from util import Errors


class Lox:
    interpreter = Interpreter()

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

    def runFile(self, path):
        with open(path) as sourceFile:
            self.run(sourceFile.readlines())

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()

        if Errors.hadError:
            return

        result = self.interpreter.interpret(statements)
        return result


if __name__ == '__main__':
    Lox().main(sys.argv)
