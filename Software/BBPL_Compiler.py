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
            equationSide = line.split("(")[1][:-2]
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
        pass

    elif "if" in line:
        # If statement
        pass

    elif "function" in line:
        # Function
        decodedAssembly.append(f"{name}:")
        decodedAssembly.append("    POP r0")
        parameters = line.split("(", maxsplit=1)[1][:-2].replace(' ', '').split(',')
        for parameter in parameters:
            decodedAssembly.append(f"    POP {parameter}")
        decodedAssembly.append("    PUSH r0")

    elif "return" in line:
        # Return
        decodedAssembly.append("    POP r0")
        returnVals = line.split("(", maxsplit=1)[1][:-1].split(',')
        for returnVal in returnVals:
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

    elif tokenInLine:
        # Calculation

        # this will go left to right
        sides = line.split("=", maxsplit=1)
        sides[1] = sides[1].strip()[1:-1]
        sides[0] = sides[0].strip()

        equationSide = shlex.split(sides[1], posix=False)

        expressionAssembly = expression(equationSide)
        for codeLine in expressionAssembly:
            decodedAssembly.append(codeLine)

        decodedAssembly.append(f"    LDR {sides[0]} acc")

    return decodedAssembly

def expression(equationSide: list[str]) -> list[str]:
    decodedAssembly = []

    decodedAssembly.append("    LDR acc " + equationSide[0])
    equationSide = equationSide[1:]
    lastVal = None
    getNextVal = False
    for val in equationSide:
        if getNextVal:
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
    
        if val in tokens:
            getNextVal = True
        lastVal = val

    return decodedAssembly

def main():
    print("Welcome to the BBPL Compiler")
    fileName = "fibbonachi.bbpl" # getFile()
    assembly = decode(fileName)
    writeFile(fileName, assembly)

    print("Complete")

if __name__ == "__main__":
    main()