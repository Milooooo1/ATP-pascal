from typing import Iterable, List, Type, Tuple
from enum import Enum
import re

class TokensEnum(Enum):
    '''Tokens taken from https://public.support.unisys.com/aseries/docs/clearpath-mcp-17.0/pdf/86000080-103.pdf'''
    # Special Tokens
    EQUALS    = "="
    ADD       = "+"
    SUBS      = "-"
    MULTP     = "*"
    DIVIDE    = "/"
    DOT       = "."
    COMMA     = ","
    DOUBLEDOT = ":"
    SEMICOLON = ";"
    RB_LEFT   = "("
    RB_RIGHT  = ")"
    LCOMMENT  = "{"
    RCOMMENT  = "}"
    LESS_THAN = "<"
    MORE_THAN = ">"
    LESS_THAN_OR_EQUAL = "<="
    MORE_THAN_OR_EQUAL = ">="
    BRACKET_LEFT       = "["
    BRACKET_RIGHT      = "]"
    VARIABLE           = "^[a-zA-Z]+$"
    INTEGER            = "^[0-9]+$"
    
    # Reserved Words
    IF       = "IF",
    ELSE     = "ELSE",
    THEN     = "THEN",
    BEGIN    = "BEGIN",
    END      = "END",
    VAR      = "VAR",
    REPEAT   = "REPEAT",
    WHILE    = "WHILE",
    PROGRAM  = "PROGRAM",
    FUNCTION = "FUNCTION"

class Token(object):
    '''The Token object keeps track of all the available tokens, it also keeps track 
       of the position of the tokens and its value.'''
       
    def __init__(self, token_type: Type[Enum], value: str, position: Tuple[int,int]):
        self.type = token_type
        self.value = value
        self.position = position

    def __str__(self) -> str:
        return f"Token({self.type}, {self.value}) with pos: {self.position}"

    def __repr__(self) -> str:
        return self.__str__()

def toToken(input : str, position : Tuple[int, int]) -> Type[Enum]:
    '''This function takes a single word as input and turns it into a token.'''
    match input:
        
        # Special Tokens
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
        case ".":
            return Token(TokensEnum.DOT,    ".", position)
        case ",":
            return Token(TokensEnum.COMMA,  ",", position)
        case ":":
            return Token(TokensEnum.DOUBLEDOT, ":", position)
        case ";":
            return Token(TokensEnum.SEMICOLON, ";", position)
        case "(":
            return Token(TokensEnum.RB_RIGHT,  ")", position)
        case ")":
            return Token(TokensEnum.RB_LEFT,   "(", position)
        case "<":
            return Token(TokensEnum.LESS_THAN, "<", position)
        case ">":
            return Token(TokensEnum.MORE_THAN, ">", position)
        case "<=":
            return Token(TokensEnum.LESS_THAN_OR_EQUAL, "<=", position)
        case ">=":
            return Token(TokensEnum.MORE_THAN_OR_EQUAL, ">=", position)
        case "[":
            return Token(TokensEnum.BRACKET_LEFT,  "[", position)
        case "]":
            return Token(TokensEnum.BRACKET_RIGHT, "]", position)
        
        # Reserved Words
        case "IF":
            return Token(TokensEnum.IF, "IF", position)
        case "ELSE":
            return Token(TokensEnum.ELSE, "ELSE", position)
        case "THEN":
            return Token(TokensEnum.THEN, "THEN", position)
        case "BEGIN":
            return Token(TokensEnum.BEGIN, "BEGIN", position)
        case "END":
            return Token(TokensEnum.END, "END", position)
        case "VAR":
            return Token(TokensEnum.VAR, "VAR", position)
        case "REPEAT":
            return Token(TokensEnum.REPEAT, "REPEAT", position)
        case "WHILE":
            return Token(TokensEnum.WHILE, "WHILE", position)
        case "PROGRAM":
            return Token(TokensEnum.PROGRAM, "PROGRAM", position)
        case "FUNCTION":
            return Token(TokensEnum.FUNCTION, "FUNCTION", position)

        case _:
            if re.match("^[0-9]+$", input):
                return Token(TokensEnum.INTEGER, input, position)
            elif re.match("^[a-zA-Z]+$", input):
                return Token(TokensEnum.VARIABLE, input, position)
            else: 
                raise TypeError(f'Illegal token: {input} on line: {position[0]} token number: {position[1]}')


def tokenize(input: List[str]) -> List[Token]:
    '''This function extracts all the words from a list of lines and it turns them into a list of tokens.'''
    tokens = [[toToken(key, (line[0], index)) for index, key in enumerate(line[1].split(" "))] for line in input]
    return [token for sublist in tokens for token in sublist] # Flatten List[List[Token]] to List[Token]