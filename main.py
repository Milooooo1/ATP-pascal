from lexer import *
from parser import *
import sys, os
import argparse

sys.setrecursionlimit(100000)

parser = argparse.ArgumentParser(description='Pascal interpreter')
parser.add_argument("-f", "--file", required=True, type=str, help="Filepath to a Pascal file")

args = parser.parse_args()

with open(args.file, 'r') as file:
    lines = [(index+1, line.replace("\n", "")) for index, line in enumerate(file)]

lexedLines = tokenize(lines)
[print(line) for line in lexedLines]
# [[print(token) for token in tokens] and print() for tokens in lexedLines]

parser = Parser(lexedLines)
print(parser.parseLine())
print(parser.parseLine())
print(parser.parseLine())
