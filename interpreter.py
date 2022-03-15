from tokens import *
from ast_classes import *

# ==========================================================================================================
#                                             Interpreter Object
# ==========================================================================================================

class Interpreter(object):
    # __init__ :: Program -> None
    def __init__(self, programAST: Program) -> None:
        self.tree = programAST
        # self.global_scope = programAST.varDeclDict

    # visit :: AST -> Union[int, float, str, bool]
    def visit(self, node: AST) -> Union[int, float, str, bool]:
        '''The visit function calls a visit function for the specific node'''
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node) # Call the specific visitor function

    # generic_visit :: AST) -> Exception 
    def generic_visit(self, node: AST) -> Exception:
        '''When a node was found without a visit function the generic_visit() function is called'''
        raise Exception('No visit_{} method'.format(type(node).__name__))

    # visit_Program :: Program) -> None 
    def visit_Program(self, node: Program) -> None:
        '''Main function which handles the root node'''
        self.program_name = node.program_name
        self.global_scope = node.varDeclDict

        [self.visit(i) for i in node.compoundStatement]
        return "done" # return to be removed, shouldn't return anything

    # visit_Assign :: Assign) -> None 
    def visit_Assign(self, node: Assign) -> None:
        '''Assignment function assigns variables their value in the scope dict'''
        if (node.left.value in self.global_scope.keys()):
            self.global_scope[node.left.value] = self.visit(node.right)
            print(self.global_scope)
        else:
            raise Exception(f"{node.left.token} was not declared in this scope")

    # visit_Num :: AST -> Union[int, float]
    def visit_Num(self, node: AST) -> Union[int, float]:
        '''visit_Num returns the value of a Num object'''
        return node.value

    # visit_Var :: Var -> Union[int, float]
    def visit_Var(self, node: Var) -> Union[int, float]:
        '''visit_Var gets the value of a variable'''
        return self.global_scope[node.value]

    # visit_NoOp :: AST) -> None 
    def visit_NoOp(self, node: AST) -> None:
        '''visit_NoOp skips NoOp ast nodes'''
        pass

    # visit_FuncCall :: FuncCall -> Union[int, float]
    def visit_FuncCall(self, node: FuncCall) -> Union[int, float]:
        '''visit_FuncCall will handle any function calls and prosecutes the function'''
        tmp = self.global_scope 
        func = [i for i in self.tree.funcList if i.funcName == node.funcName][0]
        
        # Init local scope
        self.global_scope = func.varDeclDict 
        self.global_scope['result'] = func.returnType 
        self.global_scope.update([(funcVar.value, tmp[nodeVar.value]) if nodeVar.type == TokensEnum.VARIABLE\
                                   else (funcVar.value, nodeVar.value) 
                                   for nodeVar, funcVar in zip(node.argList, func.argList)])


        [self.visit(i) for i in func.funcCodeBlock]

        # Return result value of function
        res = self.global_scope['result']
        self.global_scope = tmp
        return res

    # visit_While :: While -> None 
    def visit_While(self, node: While) -> None:
        if self.visit(node.condition):
            [self.visit(i) for i in node.codeblock]
            self.visit_While(node)    

    # visit_IfElse :: IfElse -> None 
    def visit_IfElse(self, node: IfElse) -> None:
        if self.visit(node.condition):
            [self.visit(i) for i in node.ifBlock]
        else:
            [self.visit(i) for i in node.elseNode]

    # visit_Conditional :: Conditional -> bool 
    def visit_Conditional(self, node: Conditional) -> bool:
        '''visit_Conditional'''
        match node.conditional.type:
            case TokensEnum.LESS_THAN:
                return int(int(self.visit(node.left)) < int(self.visit(node.right)))
            case TokensEnum.MORE_THAN:
                return int(int(self.visit(node.left)) > int(self.visit(node.right)))
            case TokensEnum.LESS_THAN_OR_EQUAL:
                return int(int(self.visit(node.left)) <= int(self.visit(node.right)))
            case TokensEnum.MORE_THAN_OR_EQUAL:
                return int(int(self.visit(node.left)) >= int(self.visit(node.right)))
            case _:
                raise SyntaxError(f"Unknown operator found: {node.op}")

    # visit_BinOp :: BinOp -> Union[int, float]
    def visit_BinOp(self, node: BinOp) -> Union[int, float]:
        '''visit_BinOp'''
        match node.op.type:
            case TokensEnum.ADD:
                return int(self.visit(node.left)) + int(self.visit(node.right))
            case TokensEnum.SUBS:
                return int(self.visit(node.left)) - int(self.visit(node.right))
            case TokensEnum.MULTP:
                return int(self.visit(node.left)) * int(self.visit(node.right))
            case TokensEnum.DIVIDE:
                return float(self.visit(node.left)) / float(self.visit(node.right))
            case _:
                raise SyntaxError(f"Unknown operator found: {node.op}")

    # interpret :: None
    def interpret(self) -> None:
        print(self.visit(self.tree))