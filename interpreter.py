from tokens import *
from ast_classes import *

# ==========================================================================================================
#                                             Interpreter Object
# ==========================================================================================================

class Interpreter(object):
    def __init__(self, programAST: Program) -> None:
        self.programAST = programAST