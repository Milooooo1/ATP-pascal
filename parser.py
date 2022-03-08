from token import DOT
from typing import List, Dict, Type, Tuple, Union, Optional
from lexer import *
import os

# ==========================================================================================================
#                                               AST OBJECTS
# ==========================================================================================================

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
        return f"ASSIGN: {self.left} {self.op.value} {self.right}"

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
    '''If Else object, if has a conditional and a codeBlock, else just has an code block'''
    def __init__(self, condition: Conditional, block: List[AST], elseNode: Union[AST, None]) -> None:
        self.condition = condition
        self.ifBlock = block
        self.elseNode = elseNode

    def __str__(self) -> str:
        n = "\n\t"
        return f"\nIF ({self.condition}):\n\t{[str(i) for i in self.ifBlock]}\
                 \nELSE: \n\t{[str(i) for i in self.elseNode]}\n"

class Func(AST):
    '''Function object'''
    def __init__(self, funcName: str, argList: List[Token], varDeclDict: Dict[Var, Token], funcCodeBlock: List[AST], returnType: Token) -> None:
        self.funcName = funcName.value
        self.argList = argList
        self.varDeclDict = varDeclDict
        self.funcCodeBlock = funcCodeBlock
        self.returnType = returnType

    def __str__(self) -> str:
        return f"FUNCTION \"{self.funcName}\" \
            \n\tDECLARED VARS {[str(str(i.value) + str(' = ') + str(self.varDeclDict[i].value)) for i in self.varDeclDict.keys()]}\
            \n\tRETURN TYPE: ({self.returnType.value}) \
            \n\tAND FUNCTION BLOCK: {[str(entry) for entry in self.funcCodeBlock]}"

class Program(AST):
    '''
    The Var object takes any variable
    '''
    def __init__(self, programName: str, varDecl: AST, functionsList: List[Func], compoundStatement: List[AST]) -> None:
        self.program_name = programName.value
        self.varDeclDict = varDecl
        self.funcList = functionsList
        self.compoundStatement = compoundStatement

    def __str__(self) -> str:
        return f"\nPROGRAM: \"{self.program_name}\" \
            \nDECLARED VARS {[str(str(i.value) + str(' = ') + str(self.varDeclDict[i].value)) for i in self.varDeclDict.keys()]} \
            \nDECLARED FUNCTIONS: {[str(i.funcName) for i in self.funcList]}\
            \nMAIN BODY:\n{os.linesep.join(str(i) for i in self.compoundStatement)}"

class NoOp(AST):
    '''No operation'''
    def __init__(self, token: Token) -> None:
        self.token = token

    def __str__(self) -> str:
        return f"Couldn't create an AST with token: {self.token.value}"

class Comment(AST):
    '''Comment object'''
    def __init__(self, comment: List[str]) -> None:
        self.commentLst = comment

    def __str__(self) -> str:
        return ""
        # comments = " ".join([str(item) for item in self.commentLst[1:-1]])
        # return f"COMMENT: {comments}"

# ==========================================================================================================
#                                            PARSER OBJECT
# ==========================================================================================================

class Parser(object):
    def __init__(self, lexed_tokens: List[Token]) -> None:
        self.lexed_tokens = lexed_tokens[1:]
        self.current_token = lexed_tokens[0]
        self.current_indentation = 0

    def getNextToken(self) -> Token:
        '''Pop the next token from the fron of the lexed_tokens list'''
        if len(self.lexed_tokens) == 1:
            return self.lexed_tokens[0]
        else:
            head, *tail = self.lexed_tokens
            self.lexed_tokens = tail
            return head

    def checkAndAdvance(self, token_type: TokensEnum) -> None:
        '''Check if the given token is actually the current token before advancing'''
        if self.current_token.type == token_type:
            self.current_token = self.getNextToken()
            
            if self.current_token.type == TokensEnum.LCOMMENT:
                self.comment([], self.current_token)

            if self.current_token.type == TokensEnum.WHITESPACE:
                self.removeTokenUntil(TokensEnum.WHITESPACE)

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

    def removeTokenUntil(self, token_type: TokensEnum, ctr = 0) -> Token:
        if self.current_token.type == token_type:
            self.checkAndAdvance(token_type)
            ctr += 1
            return self.removeTokenUntil(token_type, ctr)
        else:
            return ctr

    def codeBlock(self, blockLst: List[AST]) -> List[AST]:
        '''Create a block based on indentations'''
        if self.current_token.type != TokensEnum.INDENT or self.current_token == TokensEnum.ELSE:
            return blockLst
        self.removeTokenUntil(TokensEnum.INDENT)

        if self.current_token.type != TokensEnum.ELSE:
            blockLst.append(self.arithmeticExpr())
        return self.codeBlock(blockLst)

    def compoundStatement(self, blockLst: List[AST] = [], endingToken: TokensEnum = TokensEnum.SEMICOLON) -> List[AST]:
        '''This function constructs a code block or compount statement it assumes a BEGIN
        token has been encountered and constructs a code block until an ending token is encountered'''
        self.removeTokenUntil(TokensEnum.WHITESPACE)
        if self.current_token.type == TokensEnum.END and self.peek().type == endingToken:
            self.checkAndAdvance(TokensEnum.END)
            self.checkAndAdvance(endingToken)
            return blockLst

        blockLst.append(self.arithmeticExpr())
        return self.compoundStatement(blockLst, endingToken)

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
            elseBlock = self.compoundStatement([])
        return IfElse(conditional, ifBlock, elseBlock)

    def varDecl(self, varDict: Dict[Var, TokensEnum] = {}):
        '''This function creates a variable declaration block'''
        if self.current_token.type == TokensEnum.BEGIN:
            self.checkAndAdvance(TokensEnum.BEGIN)
            return varDict

        elif self.current_token.type == TokensEnum.INDENT:
            self.checkAndAdvance(TokensEnum.INDENT)

        if self.current_token.type == TokensEnum.WHITESPACE:
            self.checkAndAdvance(TokensEnum.WHITESPACE)

        if self.current_token.type == TokensEnum.VARIABLE:
            var = Var(self.current_token)
            self.checkAndAdvance(TokensEnum.VARIABLE)
            self.checkAndAdvance(TokensEnum.DOUBLEDOT)
            varDict[var] = self.current_token
            self.current_token = self.getNextToken()
            self.checkAndAdvance(TokensEnum.SEMICOLON)

        return self.varDecl(varDict)

    def constructArgList(self, argList: List[Token] = []) -> List[Token]:
        '''This function constructs an argument list which is part of constructing a function'''
        if self.current_token.type == TokensEnum.RPAREN:
            self.checkAndAdvance(TokensEnum.RPAREN)
            return argList

        argList.append(self.current_token)
        self.checkAndAdvance(TokensEnum.VARIABLE)
        if self.current_token.type == TokensEnum.COMMA:
            self.checkAndAdvance(TokensEnum.COMMA)
        return self.constructArgList(argList)

    def constructFuncList(self, funcList: List[Func] = []) -> List[Func]:
        '''Create a list of all functions'''
        if self.current_token.type != TokensEnum.FUNCTION:
            return funcList
        funcList.append(self.constructFunction())
        return self.constructFuncList(funcList)

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
        
        varDeclDict = {}
        if self.current_token.type == TokensEnum.VAR:
            self.checkAndAdvance(TokensEnum.VAR)
            varDeclDict = self.varDecl(varDeclDict)

        if self.current_token.type == TokensEnum.BEGIN:
            self.checkAndAdvance(TokensEnum.BEGIN)
        codeBlock = self.compoundStatement([], TokensEnum.SEMICOLON)

        return Func(funcName, argList, varDeclDict, codeBlock, returnType)

    # END OF HELPER FUNCTIONS

    def arithmeticExprStart(self) -> Optional[AST]:
        '''Construct arithmetic expression starting with integrals or parentheses.'''
        token = self.current_token

        if token.type == TokensEnum.INDENT:
            self.checkAndAdvance(TokensEnum.INDENT)
            token = self.current_token
            if token.type == TokensEnum.END:
                return None
            return self.arithmeticExpr()

        if token.type == TokensEnum.WHITESPACE:
            self.checkAndAdvance(TokensEnum.WHITESPACE)
            token = self.current_token
            return self.arithmeticExpr()

        # First remove any comments
        if token.type == TokensEnum.LCOMMENT:
            return self.comment([], token)

        # Check for any if else statements
        elif token.type == TokensEnum.IF:
            return self.constructIfElseExpr()

        # Check for functions
        elif token.type == TokensEnum.FUNCTION:
            return self.constructFunction()

        # Check for any assignment expressions
        elif token.type == TokensEnum.VARIABLE and self.peek().type == TokensEnum.EQUALS:
            return self.assignmentExpr()

        # Check for any conditional expressions
        elif token.type in [TokensEnum.VARIABLE, TokensEnum.INTEGER] and self.peek().type.value in TokensEnum.CONDITIONALS.value:
            return self.conditionalExpr()

        # An arithmetic expression can start with an int, var or parentheses
        elif token.type == TokensEnum.INTEGER:
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

        return NoOp(token)

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

    def parseProgram(self):
        self.checkAndAdvance(TokensEnum.PROGRAM)
        program_name = self.current_token
        self.checkAndAdvance(TokensEnum.VARIABLE)
        self.checkAndAdvance(TokensEnum.SEMICOLON)
        self.removeTokenUntil(TokensEnum.WHITESPACE)
        functionsList = []
        if self.current_token.type == TokensEnum.FUNCTION:
            functionsList = self.constructFuncList()
        self.checkAndAdvance(TokensEnum.VAR)
        var_decl = self.varDecl()
        code_block = self.compoundStatement(endingToken = TokensEnum.DOT)
        return Program(program_name, var_decl, functionsList, code_block)
