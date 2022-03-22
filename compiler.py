from io import TextIOWrapper
from tokens import *
from ast_classes import *
from interpreter import Interpreter
import os

# ==========================================================================================================
#                                              Compiler Object
# ==========================================================================================================

class Compiler(object):

    # __init__ :: Program -> None
    def __init__(self, programAST: Program) -> None:
        self.tree = programAST
        self.current_scope = dict()

    # visit :: AST -> TextIOWrapper -> Union[int, float, str, bool]
    def visit(self, node: AST, file: TextIOWrapper) -> str:
        '''The visit function calls a visit function for the specific node'''
        method_name = "compile_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, file) # Call the specific visitor function

    # generic_visit :: AST -> TextIOWrapper -> Exception 
    def generic_visit(self, node: AST, file: TextIOWrapper) -> Exception:
        '''When a node was found without a visit function the generic_visit() function is called'''
        return file.write("\t" + str(type(node).__name__) + "\n")
        # raise Exception(f"No visit_{type(node).__name__} method")

    # compile_NoOp :: NoOp -> TextIOWrapper -> None
    def compile_NoOp(self, node: NoOp, file: TextIOWrapper) -> None:
        pass

    # compile_Num :: Num -> int
    def compile_Num(self, node: Num, file: TextIOWrapper) -> int:
        '''Return num value'''
        return f"#{node.value}"

    # compile_Var :: Var -> TextIOWrapper -> str -> str
    def compile_Var(self, node: Var, file: TextIOWrapper, destRegister: str = 'R0') -> str:
        '''Load a var from the stack'''
        file.write(f"\tLDR {destRegister} [SP, #{self.current_scope[node.value] - 4}]\t\t# {node.value} loaded\n")
        return destRegister
    
    # compile_BinOp :: BinOp -> TextIOWrapper -> None
    def compile_BinOp(self, node: BinOp, file: TextIOWrapper, destRegister: str = "R0") -> None:
        '''Construct BinOp'''
        opToAsm = {"+" : "ADD", "-" : "SUB", "*" : "MUL"}

        if isinstance(node.left, BinOp) and not isinstance(node.right, BinOp):
            self.compile_BinOp(node.left, file)
            file.write(f"\t{opToAsm[node.op.value]} R0 R0 {self.visit(node.right, file)}\n")
        elif not isinstance(node.left, BinOp) and isinstance(node.right, BinOp):
            self.compile_BinOp(node.right, file)
            file.write(f"\t{opToAsm[node.op.value]} R0 R0 {self.visit(node.left, file)}\n")
        elif isinstance(node.left, BinOp) and isinstance(node.right, BinOp):
            self.compile_BinOp(node.left, file, "R3")
            self.compile_BinOp(node.right, file, "R4")
            file.write(f"\t{opToAsm[node.op.value]} {destRegister} R3 R4\n")
        elif isinstance(node.left, Num) and isinstance(node.right, Num):
            tmp = Interpreter(self.tree)
            res = tmp.visit_BinOp(node)
            file.write(f"\tMOV {destRegister} {res}\n")
        elif not isinstance(node.left, BinOp) and not isinstance(node.right, BinOp):
            file.write(f"\tMOV R1 {self.visit(node.left, file)}\n")
            file.write(f"\tMOV R2 {self.visit(node.right, file)}\n")
            file.write(f"\t{opToAsm[node.op.value]} {destRegister} R1 R2\n")

        # if isinstance(node.left, Var):
        #     self.compile_Var(node.left, file, "R1")
        # elif isinstance(node.left, Num):
        #     file.write(f"\tMOV R1 #{node.left.value}\n") 
        # elif isinstance(node.left, BinOp):
        #     self.compile_BinOp(node.left, file) 
        
        # if isinstance(node.right, Var):
        #     self.compile_Var(node.right, file, "R2")
        # elif isinstance(node.right, Num):
        #     file.write(f"\tMOV R2 #{node.right.value}\n") 
        # elif isinstance(node.right, BinOp):
        #     self.compile_BinOp(node.right, file)

        # match node.op.type:
        #     case TokensEnum.ADD:
        #         file.write(f"\tADD R0 R1 R2\n")
        #     case TokensEnum.SUBS:
        #         file.write(f"\tSUB R0 R1 R2\n")
        #     case TokensEnum.MULTP:
        #         file.write(f"\tMUL R0 R1 R2\n")

        # match node.op.type:
        #     case TokensEnum.ADD:
        #         file.write(f"\tADD {destRegister} {self.visit(node.left, file) if not isinstance(node.left, BinOp) else str('R1')} {self.visit(node.right, file) if not isinstance(node.right, BinOp) else str('R0')}\n")
        #     case TokensEnum.SUBS:
        #         file.write(f"\tSUB {destRegister} {self.visit(node.left, file) if not isinstance(node.left, BinOp) else str('R1')} {self.visit(node.right, file) if not isinstance(node.right, BinOp) else str('R0')}\n")
        #     case TokensEnum.MULTP:
        #         file.write(f"\tMUL {destRegister} {self.visit(node.left, file) if not isinstance(node.left, BinOp) else str('R1')} {self.visit(node.right, file) if not isinstance(node.right, BinOp) else str('R0')}\n")
            
    # compile_Assign :: Assign -> TextIOWrapper -> None
    def compile_Assign(self, node: Assign, file: TextIOWrapper) -> None:
        '''Store a var'''
        res = self.visit(node.right, file)
        if (res is not None):
            file.write(f"\tMOV R0 {res}\n")
        file.write(f"\tSTR R0 [SP, #{self.current_scope[node.left.value] - 4}]\t\t# {node.left.value} stored\n")

    # compileFunction :: Func -> TextIOWrapper -> str
    def compile_Func(self, funcNode: Func, file: TextIOWrapper) -> str:
        '''Compile function'''
        file.write(".thumb_func\n" + funcNode.funcName + ":\n")
        [self.visit(node, file) for node in funcNode.funcCodeBlock]
        file.write("\n")

    # compile_LocalScope :: Dict -> TextIOWrapper -> None
    def compile_LocalScope(self, scope: Dict, file: TextIOWrapper) -> None:
        file.write(f"\tSUB SP SP #{max(scope.values())}\n")

    # destruct_LocalScope :: Dict -> TextIOWrapper -> None
    def destruct_LocalScope(self, scope: Dict, file: TextIOWrapper) -> None:
        file.write(f"\tADD SP SP #{max(scope.values())}\n")

    # compiler_Program :: Program -> TextIOWrapper -> None
    def compile_Program(self, node: Program, file: TextIOWrapper) -> None:
        '''Compile the root node (Program node) of the tree'''
        file.write("\t.cpu cortex-m0\n\t.text\n\t.align 4")
        [file.write("\n\t.global " + f.funcName) for f in node.funcList]
        file.write("\n\n")
        [self.current_scope.update({var : ((index + 1) * 4)})\
                    for index, var, in enumerate(node.varDeclDict.keys())]
        self.current_scope['result'] = 0
        
        # Compile all functions
        [self.visit(funcNode, file) for funcNode in node.funcList]
        
        # Compile main
        file.write(f"{node.program_name}:\n")
        self.compile_LocalScope(self.current_scope, file)
        [self.visit(node, file) for node in node.compoundStatement]
        self.destruct_LocalScope(self.current_scope, file)

    # compile :: str -> None
    def compile(self, outFile: str) -> None:
        file = open(outFile, 'w')
        self.visit(self.tree, file)
        file.close()
        os.system(f"cat {outFile}")
        print("Compiling done.")