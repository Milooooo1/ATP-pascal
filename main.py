#!/usr/bin/python
from lexer import *
import sys, os
import argparse
import numpy as np

sys.setrecursionlimit(100000)

parser = argparse.ArgumentParser(description='Pascal interpreter')
parser.add_argument("-f", "--file", required=True, type=str, help="Filepath to a Pascal file")

args = parser.parse_args()

with open(args.file, 'r') as file:
    lines = [(index+1, line.replace("\n", "")) for index, line in enumerate(file)]

tokens = tokenize(lines)
for token in tokens:
    print(token)