from io import TextIOWrapper
from tokens import *
from ast_classes import *
import os

# ==========================================================================================================
#                                              Compiler Object
# ==========================================================================================================

class Compiler(object):

    # __init__ :: Program -> None
    def __init__(self, programAST: Program) -> None:
        self.tree = programAST

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

    # compile_Num :: Num -> int
    def compile_Num(self, node: Num, file: TextIOWrapper) -> int:
        '''Return num value'''
        return node.value

    # compile_BinOp :: BinOp -> TextIOWrapper -> None
    def compile_BinOp(self, node: BinOp, file: TextIOWrapper) -> None:
        '''Construct BinOp'''
        file.write("\tBinOp:\n")
        match node.op.type:
            case TokensEnum.ADD:
                file.write(f"\t{self.visit(node.left, file)} + {self.visit(node.right, file)}\n")

        

    # compile_Var :: Var -> TextIOWrapper -> int
    def compile_Var(self, node: Var, file: TextIOWrapper) -> int:
        '''Return variable value'''
        file.write(node.value)

    # compileFunction :: Func -> TextIOWrapper -> str
    def compile_Func(self, funcNode: Func, file: TextIOWrapper) -> str:
        '''Compile function'''
        file.write(".thumb_func\n" + funcNode.funcName + ":\n")
        [self.visit(node, file) for node in funcNode.funcCodeBlock]
        file.write("\n")

    # compiler_Program :: Program -> TextIOWrapper -> None
    def compile_Program(self, node: Program, file: TextIOWrapper) -> None:
        '''Compile the root node (Program node) of the tree'''
        file.write("\t.cpu cortex-m0\n\t.text\n\t.align 4")
        [file.write("\n\t.global " + f.funcName) for f in node.funcList]
        file.write("\n\n")
        [self.visit(funcNode, file) for funcNode in node.funcList]
        file.write(f"{node.program_name}:\n")
        [self.visit(node, file) for node in node.compoundStatement]

    # compile :: str -> None
    def compile(self, outFile: str) -> None:
        file = open(outFile, 'w')
        self.visit(self.tree, file)
        file.close()
        os.system(f"cat {outFile}")
        print("Compiling done.")