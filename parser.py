from typing import List, Type, Tuple, Union, Optional
from lexer import *
import os

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

class UnaryOp(AST):
    '''
    Unary operator

    A unary operator only needs one operand to function
    '''
    def __init__(self, op: Token, expr: Token) -> None:
        self.token = self.op = op
        self.expr = expr

    def __str__(self) -> str:
        return f"{self.token}"

class Num(AST):
    '''
    The Num object takes any literal number
    '''
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __str__(self) -> str:
        return f"{self.token.value}"

class Var(AST):
    '''
    The Var object takes any variable
    '''
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __str__(self) -> str:
        return f"VAR: {self.value}"

class Assign(AST):
    '''
    The assignment operator takes any variable and assigns any num object to it
    '''
    def __init__(self, left: Var, op: Token, right: Union[Num, BinOp]) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"ASSIGN: {self.left.value} {self.op.value} {self.right}"

class Conditional(AST):
    '''
    The conditional evaluates the lhs and rhs token with the confitional operator
    this can be a <,<=,>= or >
    '''
    def __init__(self, left: Union[Var, Num, BinOp], conditional: Token, right: Union[Var, Num, BinOp]) -> None:
        self.left = left
        self.conditional = conditional
        self.right = right

    def __str__(self) -> str:
        return f"EVAL: LHS:({self.left}) COND: {self.conditional.value}, RHS:({self.right})"

class IfElse(AST):
    def __init__(self, condition: Conditional, block: List[AST], elseNode: Union[AST, None]) -> None:
        self.condition = condition
        self.block = block
        self.elseNode = elseNode
    
    def __str__(self) -> str:
        n = "\n\t"
        return f"IF ({self.condition}):\n\t{n.join(str(line) for line in self.block)} \nELSE: \n\t{n.join(str(line) for line in self.elseNode)}"

class Func(AST):
    def __init__(self, funcName: str, argList: List[Token], beginToken: Token, funcCodeBlock: List[AST], endToken: Token, returnType: Token) -> None:
        self.funcName = funcName
        self.beginToken = beginToken
        self.funcCodeBlock = funcCodeBlock
        self.endToken = endToken
        self.returnType = returnType

    def __str__(self) -> str:
        return f"FUNCTION ({self.funcName.value}) RETURN TYPE: ({self.returnType.value}) AND FUNCTION BLOCK: {[str(entry) for entry in self.funcCodeBlock]}"

class Comment(AST):
    def __init__(self, comment: List[str]) -> None:
        self.commentLst = comment

    def __str__(self) -> str:
        comments = " ".join([str(item) for item in self.commentLst[1:-1]]) 
        return f"COMMENT: {comments}"

class Parser(object):
    def __init__(self, lexed_tokens: List[Token]) -> None:
        self.lexed_tokens = lexed_tokens[1:]
        self.current_token = lexed_tokens[0]

    def getNextToken(self) -> Token:
        head, *tail = self.lexed_tokens
        self.lexed_tokens = tail
        return head

    def checkAndAdvance(self, token_type: TokensEnum) -> None:
        if self.current_token.type == token_type:
            self.current_token = self.getNextToken()
        else:
            print(f"ERROR: {self.current_token.type} != {token_type} ON: {self.current_token.position}")

    def peek(self) -> Token:
        '''Take a lok at the next element'''
        return self.lexed_tokens[0]

    def comment(self, commentList: List[str], token: Token):
        '''Extract comments'''
        if token.type == TokensEnum.RCOMMENT:
            commentList.append(token.value)
            self.current_token = self.getNextToken()    
            return Comment(commentList)
        commentList.append(token.value)
        self.current_token = self.getNextToken()
        return self.comment(commentList, self.current_token)

    def conditionalExpr(self) -> Optional[Conditional]:
        '''Construct a conditional expression'''
        match self.current_token.type:
            case TokensEnum.VARIABLE:
                lhs = Var(self.current_token)
                self.checkAndAdvance(TokensEnum.VARIABLE)
            case TokensEnum.INTEGER:
                lhs = Num(self.current_token)
                self.checkAndAdvance(TokensEnum.INTEGER)
        
        token = self.current_token
        self.current_token = self.getNextToken()

        return Conditional(lhs, token, self.arithmeticExpr())
    
    def assignmentExpr(self) -> Optional[Assign]:
        '''Constuct an assignment expression.'''
        lhs = Var(self.current_token)
        self.checkAndAdvance(TokensEnum.VARIABLE)
        token = self.current_token
        self.checkAndAdvance(TokensEnum.EQUALS)
        return Assign(lhs, token, self.arithmeticExpr())

    def codeBlock(self, blockLst: List[AST]) -> List[AST]:
        '''Create a block based on indentations'''
        if self.current_token.type != TokensEnum.INDENT:
            return blockLst
        self.checkAndAdvance(TokensEnum.INDENT)
        blockLst.append(self.arithmeticExpr())
        return self.codeBlock(blockLst)

    def constructIfElseExpr(self) -> Optional[IfElse]:
        '''Construct an if else code block.'''
        self.checkAndAdvance(TokensEnum.IF)
        self.checkAndAdvance(TokensEnum.LPAREN)
        conditional = self.conditionalExpr()
        self.checkAndAdvance(TokensEnum.RPAREN)
        self.checkAndAdvance(TokensEnum.THEN)
        ifBlock = self.codeBlock([])
        elseBlock = []
        if self.current_token.type == TokensEnum.ELSE:
            self.checkAndAdvance(TokensEnum.ELSE)
            elseBlock = self.codeBlock([])
        return IfElse(conditional, ifBlock, elseBlock)

    def constructArgList(self, argList: List[Token] = []) -> List[Token]:
        if self.current_token.type == TokensEnum.RPAREN:
            self.checkAndAdvance(TokensEnum.RPAREN)
            return argList

        argList.append(self.current_token)
        self.checkAndAdvance(TokensEnum.VARIABLE)
        if self.current_token.type == TokensEnum.COMMA:
            self.checkAndAdvance(TokensEnum.COMMA)
        return self.constructArgList(argList)

    def constructFunction(self) -> Optional[Func]:
        '''Construct a function AST class'''
        self.checkAndAdvance(TokensEnum.FUNCTION)
        funcName = self.current_token
        self.checkAndAdvance(TokensEnum.VARIABLE)
        self.checkAndAdvance(TokensEnum.LPAREN)
        argList = self.constructArgList()
        self.checkAndAdvance(TokensEnum.DOUBLEDOT)
        returnType = self.current_token
        self.current_token = self.getNextToken()
        self.checkAndAdvance(TokensEnum.SEMICOLON)
        beginToken = self.current_token
        self.checkAndAdvance(TokensEnum.BEGIN)
        codeBlock = self.codeBlock([])
        endToken = self.current_token
        self.checkAndAdvance(TokensEnum.END)
        self.checkAndAdvance(TokensEnum.SEMICOLON)
        return Func(funcName, argList, beginToken, codeBlock, endToken, returnType)

    def arithmeticExprStart(self) -> AST:
        '''Construct arithmetic expression starting with integrals or parentheses.'''
        token = self.current_token

        # First remove any comments
        if token.type == TokensEnum.LCOMMENT:
            return self.comment([], token)

        # Check for any if else statements
        if token.type == TokensEnum.IF:
            return self.constructIfElseExpr()

        if token.type == TokensEnum.FUNCTION:
            return self.constructFunction()

        # Check for any assignment expressions
        if token.type == TokensEnum.VARIABLE and self.peek().type == TokensEnum.EQUALS:
            return self.assignmentExpr()
        # Check for any conditional expressions
        elif token.type in [TokensEnum.VARIABLE, TokensEnum.INTEGER] and self.peek().type.value in TokensEnum.CONDITIONALS.value:
            return self.conditionalExpr()

        # An arithmetic expression can start with an int, var or parentheses
        if token.type == TokensEnum.INTEGER:
            self.checkAndAdvance(TokensEnum.INTEGER)
            return Num(token)
        elif token.type == TokensEnum.VARIABLE:
            self.checkAndAdvance(TokensEnum.VARIABLE)
            return Var(token)
        elif token.type == TokensEnum.LPAREN:
            self.checkAndAdvance(TokensEnum.LPAREN)
            node = self.arithmeticExpr()
            self.checkAndAdvance(TokensEnum.RPAREN)
            return node

    def arithmeticExprHighPrecedence(self) -> AST:
        '''Construct arithmetic expression with high precedence.'''

        # Arithmetic expression must start with an integral type or precedence declaration.
        node = self.arithmeticExprStart()

        if self.current_token.type in (TokensEnum.MULTP, TokensEnum.DIVIDE):
            token = self.current_token
            self.current_token = self.getNextToken()

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
            self.current_token = self.getNextToken()

            node = BinOp(left=node, op=token, right=self.arithmeticExprHighPrecedence())

        # Before returning binary operators check if its used in a conditional
        if isinstance(node, BinOp) and self.current_token.type.value in TokensEnum.CONDITIONALS.value:
            token = self.current_token
            self.current_token = self.getNextToken()
            node = Conditional(node, token, self.arithmeticExpr())

        return node

    def parseLine(self):
        return self.arithmeticExpr()
