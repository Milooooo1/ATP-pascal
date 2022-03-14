from tokens import *
from ast_classes import *

# ==========================================================================================================
#                                             Interpreter Object
# ==========================================================================================================

class Interpreter(object):
    def __init__(self, programAST: Program) -> None:
        self.tree = programAST
        # self.global_scope = programAST.varDeclDict

    def visit(self, node: AST):
        '''The visit function calls a visit function for the specific node'''
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node) # Call the specific visitor function

    def generic_visit(self, node: AST):
        '''When a node was found without a visit function the generic_visit() function is called'''
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_Program(self, node) -> None:
        '''Main function which handles the root node'''
        self.program_name = node.program_name
        self.global_scope = node.varDeclDict

        [self.visit(i) for i in node.compoundStatement]
        return "done" # return to be removed, shouldn't return anything

    def visit_Assign(self, node: Assign) -> None:
        '''Assignment function assigns variables their value in the scope dict'''
        if (node.left.value in self.global_scope.keys()):
            self.global_scope[node.left.value] = self.visit(node.right)
            print(self.global_scope)
        else:
            raise Exception(f"{node.left.token} was not declared in this scope")

    def visit_Num(self, node: AST) -> Union[int, float]:
        '''visit_Num returns the value of a Num object'''
        return node.value

    def visit_Var(self, node: Var) -> Union[int, float]:
        '''visit_Var gets the value of a variable'''
        return self.global_scope[node.value]

    def visit_NoOp(self, node: AST) -> None:
        '''visit_NoOp skips NoOp ast nodes'''
        pass

    def visit_FuncCall(self, node: FuncCall) -> None:
        '''visit_FuncCall will handle any function calls and prosecutes the function'''
        tmp = self.global_scope 
        func = [i for i in self.tree.funcList if i.funcName == node.funcName][0]
        # Init local scope
        self.global_scope = func.varDeclDict 
        self.global_scope['result'] = func.returnType 
        self.global_scope.update([(func.argList[i].value, node.argList[i].value) for i in range(0, len(node.argList))])

        [self.visit(i) for i in func.funcCodeBlock]

        # Return result value of function
        res = self.global_scope['result']
        self.global_scope = tmp
        return res

    def visit_BinOp(self, node: BinOp) -> Union[int, float]:
        '''visit_BinOp'''
        if node.op.type == TokensEnum.ADD:
            return int(self.visit(node.left)) + int(self.visit(node.right))
        elif node.op.type == TokensEnum.SUBS:
            return int(self.visit(node.left)) - int(self.visit(node.right))
        elif node.op.type == TokensEnum.MULTP:
            return int(self.visit(node.left)) * int(self.visit(node.right))
        elif node.op.type == TokensEnum.DIVIDE:
            return float(self.visit(node.left)) / float(self.visit(node.right))
        else:
            raise Exception(f"Unknown operator found: {node.op}")

    def interpret(self):
        print(self.visit(self.tree))