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

class Token(object):
    def __init__(self, token_type: Type[Enum], value: str, position: Tuple[int,int]):
        self.type = token_type
        self.value = value
        self.position = position

    def __str__(self) -> str:
        return f"Token({self.type}, {self.value}) with pos: {self.position}"

    def __repr__(self) -> str:
        return self.__str__()

def toToken(input : str, position : Tuple[int, int]) -> Type[Enum]:
    match input:
        case "=" | ":=":
            return Token(TokensEnum.EQUALS, "=", position)
        case "+":
            return Token(TokensEnum.ADD,    "+", position)
        case "-":
            return Token(TokensEnum.SUBS,   "-", position)
        case "*":
            return Token(TokensEnum.MULTP,  "*", position)
        case "/":
            return Token(TokensEnum.DIVIDE, "/", position)
        case _:
            if re.match("^[0-9]+$", input):
                return Token(TokensEnum.INTEGER, input, position)
            elif re.match("^[a-zA-Z]+$", input):
                return Token(TokensEnum.VARIABLE, input, position)
            else: 
                raise TypeError(f'Illegal token: {input} on line: {position[0]} token number: {position[1]}')


def tokenize(input : List[str], res : List[Token]) -> List[Token]:
    if not input:
        return res
    
    head, *tail = input
    for index, key in enumerate(head[1].split(" ")):
        res.append(toToken(key, (head[0], index)))
        
    return tokenize(tail, res)
