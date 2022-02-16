from typing import List, Type, Tuple
from lexer import *

class AST(object):
    pass

class BinOp(AST):
    def __init__(self, left: Token, op: Token, right: Token) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp: LHS: ({self.left}), TOKEN: {self.token.type}, RHS: ({self.right})"

class Num(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __str__(self):
        return f"Num: {self.token.value}"

class Var(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __str__(self):
        return "VAR"

class Assign(AST):
    def __init__(self, left: Token, op: Token, right: Token) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

        def __str__(self):
            return "ASSIGN"

class Parser(object):
    def __init__(self, lexed_tokens: List[Token]) -> None:
        self.lexed_tokens = lexed_tokens[1:]
        self.current_token = lexed_tokens[0]

    def getNextToken(self) -> Token:
        head, *tail = self.lexed_tokens
        self.lexed_tokens = tail
        return head

    def error(self) -> Exception:
        raise SyntaxError(f"Invalid syntax on line: {self.current_token.position[0]}, on index {self.current_token.position[1]}")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.getNextToken()
        else:
            self.error()

    def factor(self) -> AST:
        token = self.current_token
        if token.type == TokensEnum.INTEGER:
            self.eat(TokensEnum.INTEGER)
            return Num(token)
        elif token.type == TokensEnum.LPAREN:
            self.eat(TokensEnum.LPAREN)
            node = self.expr()
            self.eat(TokensEnum.RPAREN)
            return node

    def term(self) -> AST:
        node = self.factor()

        while self.current_token.type in (TokensEnum.MULTP, TokensEnum.DIVIDE):
            token = self.current_token
            if token.type == TokensEnum.MULTP:
                self.eat(TokensEnum.MULTP)
            elif token.type == TokensEnum.DIVIDE:
                self.eat(TokensEnum.DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())

        print(node)
        return node

    def expr(self) -> AST:
        node = self.term()

        while self.current_token.type in (TokensEnum.ADD, TokensEnum.SUBS):
            token = self.current_token
            if token.type == TokensEnum.ADD:
                self.eat(TokensEnum.ADD)
            elif token.type == TokensEnum.SUBS:
                self.eat(TokensEnum.SUBS)

            node = BinOp(left=node, op=token, right=self.term())

        print(node)
        return node

    def parseLine(self):
        return self.expr()
