import shlex  # noqa: N999

# This is the BBPL compiler.

# I am making this due to the difficulty of creating a much more advanced programming language like Bear.
# BBPL stands for Basic Bear Programming Language
# This has a few main features:
#   if statements
#   for loops
#   while loops
#   subroutines with parameters
#   larger expressions (for example r0 = r5 + $0010)
# This will still use the basic assembly registers as variables but it will have additional features such as if statements, for loops, while loops.
# The indicator for a special line is brackets ()
# Multi-line statements (if, for, while, subroutines) must have the name before the bracket, this is for everything included in them.
#
# One huge rule of this is DONT USE THE ACC AS A STORAGE. IT WILL GET OVERWRITTEN VERY QUICKLY
#
# Adding variables.
# These must be defined before being used. To define a variable do: '   var {name}({expression})'
# Afterwards anything with the same name will become the address correlating to the data of that variable.
# Each variable holds 2 bytes of data. This is always an int.
# The variable will be initilised with the data inside the brackets.

variables = []
variableStart = 0x0500
variableEnd = 0x0600

labelCounter = 0

def getFile() -> str:
    while True:
        fileName = input("Enter the BBPL program you would like to compile (with the extension): ")
        if fileName[-5:] != ".bbpl":
            print("The filename must have a .bear extension.")
            continue
        try:
            with open(f"Bear-16_CPU/Software/BBPL/{fileName}", "r"):
                return fileName
        except FileNotFoundError:
            print("This file does not exist")
            continue

def writeFile(fileName: str, assembly: list[str]) -> None:
    fileName = fileName[:-5] + ".asm"
    with open(f"Bear-16_CPU/Software/Assembly/{fileName}", "w") as file:
        for i in range(len(assembly)):
            line = assembly[i]
            if i != len(assembly) - 1:
                line += "\n"
            file.write(line)

def decode(fileName: str) -> list[str]:
    assembly = []
    with open(f"Bear-16_CPU/Software/BBPL/{fileName}", "r") as file:
        for line in file:
            specialLine = False
            line = line.replace('\n', '')
            if ";" in line or "(" in line:
                quote1 = False
                quote2 = False
                for indexJ in range(len(line)):
                    character = line[indexJ]
                    if character == "'":
                        quote1 = not quote1
                    elif quote1:
                        continue
                    if character == '"':
                        quote2 = not quote2
                    elif quote2:
                        continue            
                    if character == ";":
                        line = line[:indexJ]
                        break
                    elif character == "(":
                        specialLine = True
                        continue
            if line.strip() == "":
                continue

            if specialLine:
                decodedAssembly = decodeSpecial(line)
                if decodedAssembly[0] == "FAIL":
                    print("An error occurred when decoding special")
                    return ["FAIL"]
                for line in decodedAssembly:
                    assembly.append(line)
            else:
                assembly.append(line)
    return assembly

tokens = ["+", "-", "^", "|", "&", "<<", ">>", "_", "~"] # _ is for negate    
    
def decodeSpecial(line: str) -> list[str]:
    decodedAssembly = []

    tokenInLine = False
    for token in tokens:
        if token in line:
            tokenInLine = True
            break
    name = line.split(maxsplit=1)[1].split('(', maxsplit=1)[0]

    if "for" in line:
        # For loop
        if "end" in line:
            # for loop end
            decodedAssembly.append(f"    JMP {name}")
            decodedAssembly.append(f"{name}end:")
        else:
            # for loop start
            equationSide = line.split("(")[1].strip()[:-2]
            equationSide = shlex.split(equationSide, posix=False)

            expressionAssembly = expression(equationSide)
            for codeLine in expressionAssembly:
                decodedAssembly.append(codeLine)
    
            decodedAssembly.append("    PUSH acc")
            decodedAssembly.append(f"{name}:")
            decodedAssembly.append("    POP acc")
            decodedAssembly.append(f"    JEQ acc {name}end")
            decodedAssembly.append("    SUB 1")
            decodedAssembly.append("    PUSH acc")

    elif "while" in line:
        # While loop
        if "end" in line:
            decodedAssembly.append(f"    JMP {name}")
            decodedAssembly.append(f"{name}end:")
        else:
            decodedAssembly.append(f"{name}:")

            equationSide = line.split("(")[1].strip()[:-2]
            equationSide = shlex.split(equationSide, posix=False)

            expressionAssembly = logicExpression(equationSide, name)
            if expressionAssembly[0] == "FAIL": 
                print("You must only have one symbol per section of a logic expression (sections are split by combination symbols)")
                return ["FAIL"]
            for codeLine in expressionAssembly:
                decodedAssembly.append(codeLine)

    elif "if" in line:
        # If statement
        if "end" in line:
            decodedAssembly.append(f"{name}end:")
        else:
            decodedAssembly.append(f"{name}:")

            equationSide = line.split("(")[1].strip()[:-2]
            equationSide = shlex.split(equationSide, posix=False)

            expressionAssembly = logicExpression(equationSide, name)
            if expressionAssembly[0] == "FAIL": 
                print("You must only have one symbol per section of a logic expression (sections are split by combination symbols)")
                return ["FAIL"]
            for codeLine in expressionAssembly:
                decodedAssembly.append(codeLine)

    elif "function" in line:
        # Function
        decodedAssembly.append(f"{name}:")
        decodedAssembly.append("    POP r0")
        parameters = line.split("(", maxsplit=1)[1].replace(' ', '')[:-2].split(',')
        for parameter in parameters:
            if parameter in variables:
                address = "$" + hex((variables.index(parameter) + variableStart) & 0xFFFF).replace('0x', '').zfill(4)
                decodedAssembly.append("    POP acc")
                decodedAssembly.append(f"    STM acc {address}")
            else:
                decodedAssembly.append(f"    POP {parameter}")
        decodedAssembly.append("    PUSH r0")

    elif "return" in line:
        # Return
        decodedAssembly.append("    POP r0")
        returnVals = line.split("(", maxsplit=1)[1].strip()[:-1].split(',')
        for returnVal in returnVals:
            if returnVal == "":
                continue
            equationSide = shlex.split(returnVal, posix=False)

            expressionAssembly = expression(equationSide)
            for codeLine in expressionAssembly:
                decodedAssembly.append(codeLine)

            decodedAssembly.append("    PUSH acc")
        decodedAssembly.append("    PUSH r0")
        decodedAssembly.append("    RSR")

    elif "call" in line:
        # calling a function
        parameters = line.split("(", maxsplit=1)[1][:-1].split(',')
        for parameter in parameters:
            equationSide = shlex.split(parameter.strip(), posix=False)

            expressionAssembly = expression(equationSide)
            for codeLine in expressionAssembly:
                decodedAssembly.append(codeLine)

            decodedAssembly.append("    PUSH acc")
        decodedAssembly.append(f"    JSR {name}")

    elif "var" in line:
        address = ( len(variables) + variableStart) & 0xFFFF
        if address >= variableEnd:
            print(f"You must have less than {variableEnd - variableStart} variable", end="")
            if variableEnd - variableStart == 1: print(".")
            else: print("s.")

            return ["FAIL"]
        address = "$" + hex(( len(variables) + variableStart) & 0xFFFF).replace('0x', '').zfill(4)

        equationSide = line.split("(")[1].strip()[:-1]
        equationSide = shlex.split(equationSide, posix=False)

        expressionAssembly = expression(equationSide)
        for codeLine in expressionAssembly:
            decodedAssembly.append(codeLine)

        
        decodedAssembly.append(f"    STM acc {address}")

        variables.append(name)

    else:
        # Calculation

        # this will go left to right
        sides = line.split("=", maxsplit=1)
        sides[1] = sides[1].strip()[1:-1]
        sides[0] = sides[0].strip()

        equationSide = shlex.split(sides[1], posix=False)

        expressionAssembly = expression(equationSide)
        for codeLine in expressionAssembly:
            decodedAssembly.append(codeLine)

        if sides[0] in variables:
            address = "$" + hex((variables.index(sides[0]) + variableStart) & 0xFFFF).replace('0x', '').zfill(4)
            decodedAssembly.append(f"    STM acc {address}")
        else:
            decodedAssembly.append(f"    LDR {sides[0]} acc")

    return decodedAssembly

# These are restricted. Main rules are NO bitwise operators
def logicExpression(equationSide: list[str], name: str) -> list[str]:
    logicSymbols = [">", "=", ">=", "<", "<=", "!="]
    logicSymbolInvertDict = {">": "<=", "=": "!=", ">=": "<", "<": ">=", "<=": ">", "!=": "="}
    combinationSymbols = ["and", "or", "not"]

    sym = "-"
    numSyms = 0
    for i in equationSide:
        if i in logicSymbols:
            numSyms += 1
        elif i in combinationSymbols:
            numSyms = 0
        if numSyms > 1:
            return ["FAIL"]

    i = 0
    while i <= len(equationSide):
        tok = equationSide[i]
        if tok in logicSymbols:

            if i + 1 >= len(equationSide):
                equationSide.append("0")
                break
            elif equationSide[i + 1] in combinationSymbols:
                equationSide.insert(i + 1, "0")
            else:
                if equationSide[i + 1] in tokens:
                    equationSide[i] = tok
                    match equationSide[i + 1]:
                        case "-": sym = "+"
                        case _: sym = "-"
                    del equationSide[i + 1]
                    i -= 1
                else:
                    equationSide.insert(i + 2, tok)
                    equationSide[i] = sym
                    sym = "-"
        i += 1
    i = 0
    while i < len(equationSide):
        tok = equationSide[i]
        if tok == "not":
            del equationSide[i]
            while tok not in logicSymbols:
                tok = equationSide[i]
                i += 1
            equationSide[i - 1] = logicSymbolInvertDict[tok]
        i += 1

    decodedAssembly = []
    equation = []
    i = 0
    combination = "or"
    while i < len(equationSide):
        if i + 2 < len(equationSide):
            if equationSide[i + 2] in combinationSymbols:
                combination = equationSide[i + 2]

        tok = equationSide[i]
        if tok not in logicSymbols:
            if tok not in combinationSymbols:
                equation.append(tok)
        else:
            expressionAssembly = expression(equation)
            equation = []
            for codeLine in expressionAssembly:
                decodedAssembly.append(codeLine)

            if combination == "and":
                match tok:
                    case ">": decodedAssembly.append(f"    JLE acc {name}end")
                    case "=": decodedAssembly.append(f"    JNE acc {name}end")
                    case ">=": decodedAssembly.append(f"    JLT acc {name}end")
                    case "<": decodedAssembly.append(f"    JGE acc {name}end")
                    case "<=": decodedAssembly.append(f"    JGT acc {name}end")
                    case "!=": decodedAssembly.append(f"    JEQ acc {name}end")
            elif combination == "or":
                match tok:
                    case ">": decodedAssembly.append(f"    JGT acc {name}true")
                    case "=": decodedAssembly.append(f"    JEQ acc {name}true")
                    case ">=": decodedAssembly.append(f"    JGE acc {name}true")
                    case "<": decodedAssembly.append(f"    JLT acc {name}true")
                    case "<=": decodedAssembly.append(f"    JLE acc {name}true")
                    case "!=": decodedAssembly.append(f"    JNE acc {name}true")

            if i + 2 >= len(equationSide):
                if combination == "and": decodedAssembly.append(f"    JMP {name}true")
                elif combination == "or": decodedAssembly.append(f"    JMP {name}end")
            i += 1

        i += 1
        if i >= len(equationSide):
            decodedAssembly.append(f"{name}true:")

    return decodedAssembly

def expression(equationSide: list[str]) -> list[str]:
    decodedAssembly = []

    if equationSide[0] in variables:
        address = "$" + hex((variables.index(equationSide[0]) + variableStart) & 0xFFFF).replace('0x', '').zfill(4)
        decodedAssembly.append(f"    LDM acc {address}")
    else:
        decodedAssembly.append("    LDR acc " + equationSide[0])
    equationSide = equationSide[1:]
    lastVal = None
    getNextVal = False
    for val in equationSide:
        if getNextVal:
            if val in variables:
                address = "$" + hex((variables.index(val) + variableStart) & 0xFFFF).replace('0x', '').zfill(4)
                decodedAssembly.append("    PUSH r0")
                decodedAssembly.append(f"    LDM r0 {address}")
                val = "r0"

            match lastVal:
                case "+": decodedAssembly.append("    ADD " + val)
                case "-": decodedAssembly.append("    SUB " + val)
                case "^": decodedAssembly.append("    XOR " + val)
                case "|": decodedAssembly.append("    OR " + val)
                case "&": decodedAssembly.append("    AND " + val)
                case "<<": decodedAssembly.append("    LTS")
                case ">>": decodedAssembly.append("    RTS")
                case "_": decodedAssembly.append("    NEG")
                case "~": decodedAssembly.append("    NOT")
            getNextVal = False

        if lastVal in variables:
            decodedAssembly.append("    POP r0")
    
        if val in tokens:
            getNextVal = True
        lastVal = val

    return decodedAssembly

def main():
    print("Welcome to the BBPL Compiler")
    fileName = getFile()
    assembly = decode(fileName)
    if assembly[0] == "FAIL":
        print("An error occurred.")
        input("Press anything to continue...")
        return
    writeFile(fileName, assembly)

    print("Complete")

if __name__ == "__main__":
    main()