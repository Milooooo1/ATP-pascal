#!/usr/bin/python
from atp_lexer import tokenize
import sys, os
import argparse
import numpy as np

sys.setrecursionlimit(100000)
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
print(sys.path)

parser = argparse.ArgumentParser(description='Comefrom0x10 interpreter')
parser.add_argument("-f", "--file", required=True, type=str, help="Filepath to a comefromo0x10 file")

args = parser.parse_args()

with open(args.file, 'r') as file:
    lines = [(index+1, line) for index, line in enumerate(file)]

tokenize(lines)