from lexer import *
from parser import *
import sys
import argparse

def cleanLine(line: str):
    line.expandtabs(4)
    line = line.replace("\n", "")
    leading_spaces = len(line) - len(line.lstrip())
    if leading_spaces > 0:
        line = (str("INDENT ") * int(leading_spaces / 4)) + line.lstrip()
    return line

def main():
    sys.setrecursionlimit(100000)

    parser = argparse.ArgumentParser(description='Pascal interpreter')
    parser.add_argument("-f", "--file", required=True, type=str, help="Filepath to a Pascal file")

    args = parser.parse_args()

    with open(args.file, 'r') as file:
        lines = [(index+1, cleanLine(line)) for index, line in enumerate(file)]

    lexedLines = tokenize(lines)
    [print(line) for line in lexedLines]
    print()

    parser = Parser(lexedLines)
    PascalAST = parser.parseProgram()
    print(PascalAST)


if __name__ == "__main__":
    main()