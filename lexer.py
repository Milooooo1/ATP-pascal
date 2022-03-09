from typing import List, Tuple
from tokens import *
import itertools
import re

# ==========================================================================================================
#                                             Lexer functions
# ==========================================================================================================

def toToken(input: str, position: Tuple[int, int]) -> List[Token]:
    '''This function takes a single word as input and turns it into a token.'''
    # TODO: add support for parentheses next to variables or integrals
    match input:

        # Special Tokens
        case "=" | ":=":
            return [Token(TokensEnum.EQUALS,    "=", position)]
        case "+":
            return [Token(TokensEnum.ADD,       "+", position)]
        case "-":
            return [Token(TokensEnum.SUBS,      "-", position)]
        case "*":
            return [Token(TokensEnum.MULTP,     "*", position)]
        case "/":
            return [Token(TokensEnum.DIVIDE,    "/", position)]
        case ".":
            return [Token(TokensEnum.DOT,       ".", position)]
        case ",":
            return [Token(TokensEnum.COMMA,     ",", position)]
        case ":":
            return [Token(TokensEnum.DOUBLEDOT, ":", position)]
        case ";":
            return [Token(TokensEnum.SEMICOLON, ";", position)]
        case "(":
            return [Token(TokensEnum.LPAREN,    "(", position)]
        case ")":
            return [Token(TokensEnum.RPAREN,    ")", position)]
        case "[":
            return [Token(TokensEnum.BRACKET_LEFT,       "[",  position)]
        case "]":
            return [Token(TokensEnum.BRACKET_RIGHT,      "]",  position)]
        case "<":
            return [Token(TokensEnum.LESS_THAN,          "<",  position)]
        case ">":
            return [Token(TokensEnum.MORE_THAN,          ">",  position)]
        case "<=":
            return [Token(TokensEnum.LESS_THAN_OR_EQUAL, "<=", position)]
        case ">=":
            return [Token(TokensEnum.MORE_THAN_OR_EQUAL, ">=", position)]

        # Reserved Words
        case input if input.upper() == "INDENT":
            return [Token(TokensEnum.INDENT,     "INDENT",   position)]
        case input if input.upper() == "IF":
            return [Token(TokensEnum.IF,         "IF",       position)]
        case input if input.upper() == "ELSE":
            return [Token(TokensEnum.ELSE,       "ELSE",     position)]
        case input if input.upper() == "THEN":
            return [Token(TokensEnum.THEN,       "THEN",     position)]
        case input if input.upper() == "BEGIN":
            return [Token(TokensEnum.BEGIN,      "BEGIN",    position)]
        case input if input.upper() == "END":
            return [Token(TokensEnum.END,        "END",      position)]
        case input if input.upper() == "VAR":
            return [Token(TokensEnum.VAR,        "VAR",      position)]
        case input if input.upper() == "DO":
            return [Token(TokensEnum.DO,        "DO",      position)]
        case input if input.upper() == "REPEAT":
            return [Token(TokensEnum.REPEAT,     "REPEAT",   position)]
        case input if input.upper() == "WHILE":
            return [Token(TokensEnum.WHILE,      "WHILE",    position)]
        case input if input.upper() == "PROGRAM":
            return [Token(TokensEnum.PROGRAM,    "PROGRAM",  position)]
        case input if input.upper() == "FUNCTION":
            return [Token(TokensEnum.FUNCTION,   "FUNCTION", position)]
        case input if input.upper() == "INTEGER":
            return [Token(TokensEnum.RT_INTEGER, "INTEGER",  position)]

        # Non-whitespace splitted tokens
        case input if "{" in input and "}" in input:
            return [Token(TokensEnum.LCOMMENT, input[:1],    position),
                    Token(TokensEnum.VARIABLE, input[1:-1], (position[0], position[1]+1)),
                    Token(TokensEnum.RCOMMENT, input[-1:],  (position[0], position[1]+2))]

        case input if "{" in input:
            return [Token(TokensEnum.LCOMMENT, input[:1],    position),
                    Token(TokensEnum.VARIABLE, input[1:],   (position[0], position[1]+1))]

        case input if "}" in input:
            return [Token(TokensEnum.VARIABLE, input[:-1],   position),
                    Token(TokensEnum.RCOMMENT, input[-1:],  (position[0], position[1]+1))]

        case input if "(" in input:
            if input.find("(") != 0:
                return [toToken(input[:input.find("(")],     position),
                        Token(TokensEnum.LPAREN, "(",       (position[0], position[1]+1)),
                        toToken(input[input.find("(")+1:],  (position[0], position[1]+2))]
            else:
                return [Token(TokensEnum.LPAREN, "(",        position),
                         toToken(input[input.find("(")+1:], (position[0], position[1]+1))]

        case input if ")" in input:
            if input.find(")") != (len(input)-1):
                return [toToken(input[:input.find(")")],    position),
                        Token(TokensEnum.RPAREN, ")",      (position[0], position[1]+1)),
                        toToken(input[input.find(")")+1:], (position[0], position[1]+2))]
            else:
                return [toToken(input[:input.find(")")],    position),
                        Token(TokensEnum.RPAREN, ")",      (position[0], position[1]+1))]

        case input if "," in input:
            return [toToken(input[:input.find(",")], position),
                   [Token(TokensEnum.COMMA, input[input.find(","):], (position[0], position[1]+1))]]

        case input if "." in input:
            return [toToken(input[:input.find(".")], position),
                   [Token(TokensEnum.DOT, input[input.find("."):], (position[0], position[1]+1))]]

        case input if ";" in input:
            return [toToken(input[:input.find(";")], position),
                   [Token(TokensEnum.SEMICOLON, input[input.find(";"):], (position[0], position[1]+1))]]

        # Variable and literals
        case input if re.match("^[0-9]+$", input):
            return [Token(TokensEnum.INTEGER, input, position)]
        case input if re.match("^[a-zA-Z]+$", input):
            return [Token(TokensEnum.VARIABLE, input, position)]

        case '':
            return [Token(TokensEnum.WHITESPACE, input, position)]

        # Catch any invalid tokens
        case _:
            raise TypeError(f'Illegal token: {repr(input)} on line: {position[0]} token number: {position[1]}')

def flatten(lst: List) -> Token:
    if isinstance(lst, Token):
        return lst

    if len(lst) == 1:
        return lst[0]

    head, *tail = lst
    return head + flatten(tail)

def recFlatten(x):
    res = []
    def loop(y):
        for i in y:
            if isinstance(i, list):
                loop(i)
            else:
                res.append(i)
    loop(x)
    return res

def tokenize(input: List[str]) -> List[Token]:
    '''This function extracts all the words from a list of lines and it turns them into a list of tokens per line'''
    tokens = [[[entry for entry in recFlatten(toToken(key, (line[0], index)))] for index, key in enumerate(line[1].split(" "))] for line in input]
    return list(itertools.chain.from_iterable([[flatten(k) for k in token] for sublist in tokens for token in sublist]))