from tkinter import Variable
from typing import Iterable, List, Type, Tuple
from enum import Enum
import re

class TokensEnum(Enum):
    EQUALS    = "="
    ADD       = "+"
    SUBS      = "-"
    MULTP     = "*"
    DIVIDE    = "/"
    DOT       = "."
    COMMA     = ","
    DOUBLEDOT = ""
    SEMICOLON = ";"
    RB_LEFT   = "("
    RB_RIGHT  = ")"
    LESS_THAN = "<"
    MORE_THAN = ">"
    LESS_THAN_OR_EQUAL = "<="
    MORE_THAN_OR_EQUAL = "=>"
    BRACKET_LEFT       = "["
    BRACKET_RIGHT      = "]"
    VARIABLE           = "^[a-zA-Z]+$"
    INTEGER            = "^[0-9]+$"

class Token:
    def __init__(self, token_type: Type[Enum], value: str, position: Tuple[int,int]):
        self.type = token_type
        self.value = value
        self.position = position

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value}) on position: ({self.position})'

    def __repr__(self) -> str:
        return self.__str__()

# class Lexer(object):
#     reserved_words = ["program", "label", "const", "type", "procedure", "function", "var", "begin", "end", "div", "mod", "and", "not", "or", "in"]

    # def __init__(self):
    #     pass

    def tokenize(input : List[str]) -> List[str]:
        for line in input:
            print(line)

    def toToken(input : str, position : Tuple[int, int]) -> Type[Enum]:
        match input:
            case "=", ":=":
                return Token(TokensEnum.EQUALS, "=", position)
            case "+":
                return Token(TokensEnum.ADD,    "+", position)
            case "-":
                return Token(TokensEnum.SUBS,   "-", position)
            case "*":
                return Token(TokensEnum.MULTP,  "*", position)
            case "/":
                return Token(TokensEnum.DIVIDE, "/", position)
            case re.match(TokensEnum.INTEGER, input):
                return Token(TokensEnum.INTEGER, input, position)
            case re.match(TokensEnum.VARIABLE, input):
                return Token(TokensEnum.VARIABLE, input, position)
            case _:
                raise TypeError(f'Illegal character: {input}')