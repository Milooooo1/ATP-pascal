from tokens import *
from ast_classes import *

# ==========================================================================================================
#                                              Compiler Object
# ==========================================================================================================

class Compiler(object):

    # __init__ :: Program -> None
    def __init__(self, programAST: Program) -> None:
        self.tree = programAST

    # compiler :: str -> None
    def compile(self, outFile: str) -> None:
        file = open(outFile, 'w')
        file.write("\t.cpu cortex-m0\n\t.text\n\t.align 4\n")
        # compile all functions
        # compile main
        file.close()
        print("Compiling done.")