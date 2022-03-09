from typing import List, Dict, Type, Tuple, Union, Optional
from tokens import *
from os import linesep

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
        return f"EVAL: LHS:({self.left}) {self.conditional.value}, RHS:({self.right})"

class While(AST):
    '''A while loop has a condition and a codeblock to execute while the condition is true'''
    def __init__(self, condition: Conditional, block: List[AST]) -> None:
        self.condition = condition
        self.codeblock = block

    def __str__(self) -> str:
        return f"WHILE {self.condition} \n\tDO {[str(i) for i in self.codeblock]}"

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
            \nMAIN BODY:\n{linesep.join(str(i) for i in self.compoundStatement)}"

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