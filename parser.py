from typing import List, Type, Tuple
from lexer import *

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left: Token, op: Token, right: Token) -> None:
        # TODO: check for correct token types
        self.left = left
        self.token = self.op = op
        self.right = right
        
class Num(AST):
    def __init__(self, token: Token) -> None:
        # TODO: check for correct token types
        self.token = token
        self.value = self.token.value
    
class Parser(object):
    def __init__(self, lexed_tokens: List[Token]) -> None:
        self.tokenslist = lexed_tokens
        
    