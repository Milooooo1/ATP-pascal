from tokens import *
from ast_classes import *

# ==========================================================================================================
#                                              Compiler Object
# ==========================================================================================================

class Compiler(object):

    # __init__ :: Program -> None
    def __init__(self, programAST: Program) -> None:
        self.tree = programAST

    # compiler :: None
    def compile(self) -> None:
        pass