from lexer import *
from parser import *
from interpreter import *
from compiler import *
import sys
import argparse

def cleanLine(line: str):
    line.expandtabs(4)
    line = line.replace("\n", "")
    leading_spaces = len(line) - len(line.lstrip())
    if leading_spaces > 0:
        line = (str("INDENT ") * int(leading_spaces / 4)) + line.lstrip()
    return line

def main():
    sys.setrecursionlimit(100000)

    parser = argparse.ArgumentParser(description='Pascal interpreter')
    parser.add_argument("-f", "--file", required=True, type=str, help="Filepath to a Pascal file")
    parser.add_argument("-c", "--compile", required=False, action='store_true', help="Flag to specify if the file needs to be compiled or not")
    parser.add_argument("-i", "--interpret", required=False, action='store_true', help="Flag to specify if the file needs to be interpreted or not")
    parser.add_argument("-o", "--out", required=False, type=str, help="File to store the compiled code in", default="out.asm")

    args = parser.parse_args()

    with open(args.file, 'r') as file:
        lines = [(index+1, cleanLine(line)) for index, line in enumerate(file)]

    lexedLines = tokenize(lines)
    [print(line) for line in lexedLines]
    print()

    parser = Parser(lexedLines)
    PascalAST = parser.parseProgram()
    print(PascalAST)

    if args.interpret:
        print("\n\n\nInterpreting program:") # New lines for readability in terminal
        interpreter = Interpreter(PascalAST)
        interpreter.interpret()

    if args.compile:
        print("\n\n\nCompiling program:") # New lines for readability in terminal
        compiler = Compiler(PascalAST)
        outFileName = args.out
        if "." not in outFileName:
            outFileName += ".pas"

        compiler.compile(outFileName)

        # To be able to use the ASM interpreter we need to make some modifications to the code
        data = []
        with open (outFileName, "r") as myfile:
            data = myfile.readlines()

        # remove all initialization
        newFile = ''
        for line in data:
            if  ".global" in line or ".text" in line or ".text" in line or ".align" in line or ".cpu" in line:
                pass
            else:
                newFile += line
                   
        # program name must be _start
        newFile = newFile.replace(PascalAST.program_name, "_start", -1)
        file = open("ASM-Interpreter/toRun.asm", 'w')
        file.write(newFile)
        file.close()
        print("Running interpreter...")
        os.system(f"python3.6 ASM-Interpreter/main.py")

    if not args.compile and not args.interpret:
        print("Please specify if the program needs to be compiled or interpreted by passing one of the following flags:")
        print("\t-i or --interpret for interpretation")
        print("\t-c or --compile   for compilation")

if __name__ == "__main__":
    main()