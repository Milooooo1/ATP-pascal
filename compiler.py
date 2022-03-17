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

    # compileExpression :: AST -> str
    def compileExpression(self, node: AST) -> str:
        return str(type(node).__name__)

    # compileFunction :: Func -> str
    def compileFunction(self, funcNode: Func) -> str:
        outStr = funcNode.funcName + ":\n"
        [outStr := outStr + f"\t{self.compileExpression(node)}\n" for node in funcNode.funcCodeBlock]
        outStr += "\n"
        return outStr

    # compiler :: str -> None
    def compile(self, outFile: str) -> None:
        file = open(outFile, 'w')
        file.write("\t.cpu cortex-m0\n\t.text\n\t.align 4\n\t.global ")
        [file.write(f.funcName + " ") for f in self.tree.funcList]
        file.write("\n\n")
        [file.write(self.compileFunction(funcNode)) for funcNode in self.tree.funcList]
        file.write(f"{self.tree.program_name}:\n")
        [file.write(f"\t{self.compileExpression(node)}\n") for node in self.tree.compoundStatement]
        file.close()
        os.system(f"cat {outFile}")
        print("Compiling done.")