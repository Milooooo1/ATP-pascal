from typing import List, Type, Tuple
from lexer import *

class AST(object):
    pass

class BinOp(AST):
    '''
    Binary operator

    A binary operator needs two operands and an operator
    Example 1 + 2 where 1 and 2 are the operands and + is the operator
    '''
    def __init__(self, left: Token, op: Token, right: Token) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"BinOp: LHS: ({self.left}), OP: {self.token.value}, RHS: ({self.right})"

class UnaryOp(object):
    '''
    '''
    def __init__(self, op: Token, expr: Token) -> None:
        self.token = self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"{self.token}"
class Num(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __str__(self) -> str:
        return f"{self.token.value}"

class Var(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __str__(self) -> str:
        return f"{self.value}"

class Assign(AST):
    def __init__(self, left: Token, op: Token, right: Token) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

        def __str__(self) -> str:
            return f"ASSIGN: {self.right} {self.op} to {self.left}"

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

    def arithmeticExprStart(self) -> AST:
        '''Construct arithmetic expression starting with integrals or parentheses.'''
        token = self.current_token
        if token.type == TokensEnum.INTEGER:
            self.eat(TokensEnum.INTEGER)
            return Num(token)
        elif token.type == TokensEnum.LPAREN:
            self.eat(TokensEnum.LPAREN)
            node = self.arithmeticExpr()
            self.eat(TokensEnum.RPAREN)
            return node

    def arithmeticExprHighPrecedence(self) -> AST:
        '''Construct arithmetic expression with high precedence.'''

        # Arithmetic expression must start with an integral type or precedence declaration.
        node = self.arithmeticExprStart()

        if self.current_token.type in (TokensEnum.MULTP, TokensEnum.DIVIDE):
            token = self.current_token
            if token.type == TokensEnum.MULTP:
                self.eat(TokensEnum.MULTP)
            elif token.type == TokensEnum.DIVIDE:
                self.eat(TokensEnum.DIVIDE)

            node = BinOp(left=node, op=token, right=self.arithmeticExprStart())

        return node

    def arithmeticExpr(self) -> AST:
        '''Constuct arithmetic expression'''

        # First call higher precedence function
        node = self.arithmeticExprHighPrecedence()

        # After checking for higher precedence operators
        # now we can check for lower precedence operators
        if self.current_token.type in (TokensEnum.ADD, TokensEnum.SUBS):
            token = self.current_token
            if token.type == TokensEnum.ADD:
                self.eat(TokensEnum.ADD)
            elif token.type == TokensEnum.SUBS:
                self.eat(TokensEnum.SUBS)

            node = BinOp(left=node, op=token, right=self.arithmeticExprHighPrecedence())

        return node

    def parseLine(self):
        return self.arithmeticExpr()
