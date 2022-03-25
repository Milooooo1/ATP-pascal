from io import TextIOWrapper
from tokens import *
from ast_classes import *
from interpreter import Interpreter
import os
import difflib

# ==========================================================================================================
#                                              Compiler Object
# ==========================================================================================================

class Compiler(object):

    # __init__ :: Program -> None
    def __init__(self, programAST: Program) -> None:
        self.tree = programAST
        self.current_scope = dict()
        self.push = "\tPUSH {r4, r5, r6, r7, lr}\n"
        self.pop = "\tPOP {r4, r5, r6, r7, pc}\n"

    # visit :: AST -> TextIOWrapper -> str-> Union[int, str]
    def visit(self, node: AST, file: TextIOWrapper, parent: str = "") -> Union[int, str]:
        '''The visit function calls a visit function for the specific node'''
        method_name = "compile_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, file, parent) # Call the specific visitor function

    # generic_visit :: AST -> TextIOWrapper -> Exception 
    def generic_visit(self, node: AST, file: TextIOWrapper, parent) -> Exception:
        '''When a node was found without a visit function the generic_visit() function is called'''
        return file.write("\t" + str(type(node).__name__) + "\n")
        # raise Exception(f"No visit_{type(node).__name__} method")

    # compile_NoOp :: NoOp -> TextIOWrapper -> str -> None
    def compile_NoOp(self, node: NoOp, file: TextIOWrapper, parent: str = "") -> None:
        pass

    # compile_Num :: Num -> TextIOWrapper -> str -> int
    def compile_Num(self, node: Num, file: TextIOWrapper, parent: str = "") -> int:
        '''Return num value'''
        return f"#{node.value}"

    # compile_Var :: Var -> TextIOWrapper -> str -> str -> str
    def compile_Var(self, node: Var, file: TextIOWrapper, parent: str = "", destRegister: str = 'R0') -> str:
        '''Load a var from the stack'''
        file.write(f"\tLDR {destRegister}, [SP, #{self.current_scope[node.value] - 4}]\n")
        return destRegister
    
    # compile_BinOp :: BinOp -> TextIOWrapper -> str -> None
    def compile_BinOp(self, node: BinOp, file: TextIOWrapper, parent: str = "", destRegister: str = "R0") -> None:
        '''Construct BinOp'''
        opToAsm = {"+" : "ADD", "-" : "SUB", "*" : "MUL"}

        if isinstance(node.left, BinOp) and not isinstance(node.right, BinOp):
            self.compile_BinOp(node.left, file, "")
            file.write(f"\t{opToAsm[node.op.value]} {destRegister}, R0, {self.visit(node.right, file)}\n")
        elif not isinstance(node.left, BinOp) and isinstance(node.right, BinOp):
            self.compile_BinOp(node.right, file, "")
            file.write(f"\t{opToAsm[node.op.value]} {destRegister}, R0, {self.visit(node.left, file)}\n")
        elif isinstance(node.left, BinOp) and isinstance(node.right, BinOp):
            self.compile_BinOp(node.left, file, "", "R3")
            self.compile_BinOp(node.right, file, "", "R4")
            file.write(f"\t{opToAsm[node.op.value]} {destRegister}, R3, R4\n")
        elif isinstance(node.left, Num) and isinstance(node.right, Num):
            tmp = Interpreter(self.tree)
            res = tmp.visit_BinOp(node)
            file.write(f"\tMOV {destRegister}, #{res}\n")
        elif not isinstance(node.left, BinOp) and not isinstance(node.right, BinOp):
            file.write(f"\tMOV R1, {self.visit(node.left, file)}\n")
            file.write(f"\tMOV R2, {self.visit(node.right, file)}\n")
            file.write(f"\t{opToAsm[node.op.value]} {destRegister}, R1, R2\n")

    # compile_Conditional :: Construct -> TextIOWrapper -> str -> None
    def compile_Conditional(self, node: Conditional, file: TextIOWrapper, parent: str = "") -> None:
        file.write(f"\tCMP {self.visit(node.left, file)}, {self.visit(node.right, file)}\n")

    # compile_IfElse :: IfElse -> TextIOWrapper -> str -> str -> None
    def compile_IfElse(self, node: IfElse, file: TextIOWrapper, parent: str = "", function: str = "") -> None:
        opToAsm = {"==" : "BEQ",  "!=" : "BNE", "<=" : "BLE",  ">=" : "BGE", "<" : "BLT", ">" : "BHI"}
        self.visit(node.condition, file)
        condition_label = f"{node.condition.left.value}{opToAsm[node.condition.conditional.value].lower()}{node.condition.right.value}"
        file.write(f"\t{opToAsm[node.condition.conditional.value]} {parent}_{condition_label}_if\n")
        file.write(f"\tBL {parent}_{condition_label}_else\n")
        file.write("\n")

        file.write(f"{parent}_{condition_label}_if:\n")
        [self.visit(line, file, f"{parent}_{condition_label}_if") for line in node.ifBlock]
        file.write(f"\tBL {parent}_end\n")
        file.write("\n")

        file.write(f"{parent}_{condition_label}_else:\n")
        [self.visit(line, file, f"{parent}_{condition_label}_else") for line in node.elseNode]
        file.write(f"\tBL {parent}_end\n")
        file.write("\n")

        file.write(f"{parent}_end:\n")

    # compile_Assign :: Assign -> TextIOWrapper -> str -> None
    def compile_Assign(self, node: Assign, file: TextIOWrapper, parent: str = "") -> None:
        '''Store a var'''
        # If rhs of assign is a var or constant it needs to be pt into R0
        res = self.visit(node.right, file)
        if(res is not None):
            file.write(f"\tMOV R0, {res}\n")

        file.write(f"\tSTR R0, [SP, #{self.current_scope[node.left.value] - 4}]\n")

    # compile_FuncCall :: FuncCall -> TextIOWrapper -> str -> None
    def compile_FuncCall(self, node: FuncCall, file: TextIOWrapper, parent: str = "") -> None:
        try:
            if(node.funcName == "printInt"):
                file.write("\tbl print_int\n")
            else:
                # Get the first occurance of the function name
                func = [i for i in self.tree.funcList if i.funcName == node.funcName][0] 
                
                # Pass the arguments by storing them in the scratch registers
                [file.write(f"\tLDR R{index}, [SP, #{self.current_scope[arg.value]-4}]\n") if not arg.value.isnumeric() 
                else file.write(f"\tMOV R{index}, #{arg.value}\n")
                for index, arg in enumerate(node.argList)] 
                
                # Branch link to function
                file.write(f"\tBL {func.funcName}\n")
        except IndexError as e:
            close_matches = " ".join(difflib.get_close_matches(node.funcName, [func.funcName for func in self.tree.funcList]))
            if len(close_matches) != 0:
                raise IndexError(f"Function name: {node.funcName} does not exist. Did you mean any of the following functions: {close_matches}?\n")
            else:
                raise IndexError(f"Function name: {node.funcName} does not exist.\n")

    # compileFunction :: Func -> TextIOWrapper -> str -> str
    def compile_Func(self, funcNode: Func, file: TextIOWrapper, parent: str = "") -> str:
        '''Compile function'''
        file.write(funcNode.funcName + ":\n")
        
        # Update the function scope
        tmp = self.current_scope
        self.current_scope = {}
        funcNode.varDeclDict['result'] = 0
        [funcNode.varDeclDict.update({arg.value : 0}) for arg in funcNode.argList]
        [self.current_scope.update({var : ((index + 1) * 4)})\
                    for index, var, in enumerate(funcNode.varDeclDict.keys())]

        # Compile function body
        file.write(self.push)
        self.compile_LocalScope(self.current_scope, file)

        # Store given arguments on stack
        [file.write(f"\tSTR R{index}, [SP, #{self.current_scope[var.value] - 4}]\n") for index, var in enumerate(funcNode.argList)]

        [self.visit(node, file, funcNode.funcName) for node in funcNode.funcCodeBlock]
        file.write(f"\tLDR R0, [SP, #{self.current_scope['result'] - 4}]\n")
        self.destruct_LocalScope(self.current_scope, file)
        file.write(self.pop)
        file.write("\n")

        self.current_scope = tmp

    # compile_LocalScope :: Dict -> TextIOWrapper -> str -> None
    def compile_LocalScope(self, scope: Dict, file: TextIOWrapper, parent: str = "") -> None:
        file.write(f"\tSUB SP, SP, #{max(scope.values())}\n")

    # destruct_LocalScope :: Dict -> TextIOWrapper -> None
    def destruct_LocalScope(self, scope: Dict, file: TextIOWrapper) -> None:
        file.write(f"\tADD SP, SP, #{max(scope.values())}\n")

    # compiler_Program :: Program -> TextIOWrapper -> str -> None
    def compile_Program(self, node: Program, file: TextIOWrapper, parent: str = "") -> None:
        '''Compile the root node (Program node) of the tree'''
        file.write("\t.cpu cortex-m0\n\t.text\n\t.align 4")
        [file.write("\n\t.global " + f.funcName) for f in node.funcList]
        file.write("\n\n")
        node.varDeclDict['result'] = 0
        [self.current_scope.update({var : ((index + 1) * 4)})\
                    for index, var, in enumerate(node.varDeclDict.keys())]
        
        # Compile all functions
        [self.visit(funcNode, file, node.program_name) for funcNode in node.funcList]
        
        # Compile main
        file.write(f"{node.program_name}:\n")
        file.write(self.push)
        self.compile_LocalScope(self.current_scope, file)
        [self.visit(node, file, self.tree.program_name) for node in node.compoundStatement]
        self.destruct_LocalScope(self.current_scope, file)
        file.write(self.pop)

    # compile :: str -> None -> str
    def compile(self, outFile: str) -> None:
        file = open(outFile, 'w')
        self.visit(self.tree, file)
        file.close()
        # os.system(f"cat {outFile}")
        print("Compiling done.")