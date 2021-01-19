import sys

from scanner import Scanner
from util import error


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
                error('\nExiting lox')
                break

    def run(self, source):
        tokens = Scanner(source).scanTokens()
        print(tokens)


if __name__ == '__main__':
    Lox().main(sys.argv)



