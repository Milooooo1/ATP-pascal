from typing import Tuple, Type
from enum import Enum

# ==========================================================================================================
#                                                   Tokens
# ==========================================================================================================

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
    LPAREN    = "("
    RPAREN    = ")"
    LCOMMENT  = "{"
    RCOMMENT  = "}"
    COMMENT   = "{}"
    LESS_THAN = "<"
    MORE_THAN = ">"
    LESS_THAN_OR_EQUAL = "<="
    MORE_THAN_OR_EQUAL = ">="
    CONDITIONALS = [LESS_THAN, MORE_THAN, LESS_THAN_OR_EQUAL, MORE_THAN_OR_EQUAL]
    BRACKET_LEFT       = "["
    BRACKET_RIGHT      = "]"
    VARIABLE           = "^[a-zA-Z]+$"
    INTEGER            = "^[0-9]+$"

    # Reserved Words
    IF         = "IF",
    ELSE       = "ELSE",
    THEN       = "THEN",
    INDENT     = "INDENT",
    BEGIN      = "BEGIN",
    END        = "END",
    VAR        = "VAR",
    DO         = "DO",
    REPEAT     = "REPEAT",
    WHILE      = "WHILE",
    PROGRAM    = "PROGRAM",
    FUNCTION   = "FUNCTION",
    RT_INTEGER = "INTEGER",
    WHITESPACE = " "

class Token(object):
    '''The Token object keeps track of all the available tokens, it also keeps track
       of the position of the tokens and its value.'''

    def __init__(self, token_type: Type[TokensEnum], value: str, position: Tuple[int,int]) -> None:
        self.type = token_type
        self.value = value
        self.position = position

    def __str__(self) -> str:
        return f"Token({self.type}, {self.value}) with pos: {self.position}"

    def __repr__(self) -> str:
        return self.__str__()