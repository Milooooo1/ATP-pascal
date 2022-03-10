from typing import List, Dict, Optional
from tokens import *
from ast_classes import *

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

    def peek(self, index = 0) -> Token:
        '''Take a lok at the next element'''
        return self.lexed_tokens[index]

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

    def constructWhileExpr(self) -> Optional[While]:
        '''Construct a While expression'''
        self.checkAndAdvance(TokensEnum.WHILE)
        self.checkAndAdvance(TokensEnum.LPAREN)
        conditional = self.conditionalExpr()
        self.checkAndAdvance(TokensEnum.RPAREN)
        self.checkAndAdvance(TokensEnum.DO)
        self.removeTokenUntil(TokensEnum.WHITESPACE)
        self.removeTokenUntil(TokensEnum.INDENT)
        self.checkAndAdvance(TokensEnum.BEGIN)
        codeBlock = self.compoundStatement([])
        return While(conditional, codeBlock)

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
        self.current_token = self.getNextToken()
        if self.current_token.type == TokensEnum.COMMA:
            self.checkAndAdvance(TokensEnum.COMMA)
        return self.constructArgList(argList)

    def functionCall(self):
        funcName = self.current_token
        self.checkAndAdvance(TokensEnum.VARIABLE)
        self.checkAndAdvance(TokensEnum.LPAREN)
        argList = self.constructArgList([])
        return FuncCall(funcName.value, argList)

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

        # Check for any while loops
        elif token.type == TokensEnum.WHILE:
            return self.constructWhileExpr()

        # Check for functions
        elif token.type == TokensEnum.FUNCTION:
            return self.constructFunction()

        # Check for any assignment expressions
        elif token.type == TokensEnum.VARIABLE and self.peek().type == TokensEnum.EQUALS:
            return self.assignmentExpr()

        elif token.type == TokensEnum.VARIABLE and self.peek().type == TokensEnum.LPAREN:
            return self.functionCall()

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
