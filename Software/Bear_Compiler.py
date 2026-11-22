# This is the Bear Compiler

# This is a high-level programming language for the Bear-16 CPU

# Features:
# Case sensitive
# Variables:
#   Word-Based Variables: These are variables which are identified by the name.
#   Maximum of 256 Variables
#   These cannot contain special words such as "int"
#   These cannot contain spaces
# Functions
# Inline assembly
# Input via the keyboard
#   This will be done through 2 instructions, input and inchar
#   inchar will just loop until a single character has been entered but won't echo it and save it to a char.
#   input will loop until enter has been entered and will echo every character and save it to a string.
# Output via the text screen
types = ["None", "int", "bool", "char", "string", "float"]
# Types:
#   0) None
#   1) Int
#   2) Bool
#   3) Char
#   4) String
#   5) Float
#   6) Arrays
#   You have to declare the type that a variable is
# Constants
# For loops
# While loops
# If statements
#   Elseif
#   Else
# Expressions:
#   Arithmetic expressions: This will return an int or a float
#   + Addition (Adds two integers or two floats)
#   - Subtraction (Subtracts two integers or two floats)
#   & Bitwise AND (ANDs two integers or two floats)
#   | Bitwise OR (ORs two integers or two floats)
#   ~ Bitwise NOT (NOTs a integer)
#   ^ Bitwise XOR (XORs two integers or two floats)
#   >> Bitwise Right Shift (Right Shifts two integers or two floats)
#   << Bitwise Left Shift (Left Shifts two integers or two floats)

#   Boolean expressions: These will always return a boolean value
#   and (ANDs two booleans)
#   or (ORs two booleans)
#   not (NOTs a boolean)
#   xor (XORs two booleans)
#   < Less than (Less than compares two of the same type)
#   > Greater than (Greater than compares two of the same type)
#   = Equals (Equals compares two of the same type)
#   <= Greater than or Equal (Greater than or Equal compares two of the same type)
#   >= Less than or Equal (Less than or Equal compares two of the same type)
#   != Not Equals (Not Equals compares two of the same type)

#   String expressions: These will always return a string value
#   + Conjugation (Combines two strings)
#   .len (SPEICAL CASE: RETURNS A integer. This returns the length of a string as an integer.)
#   [] Addressing (Uses an integer and a string and returns the letter at the address of the integer)
# Peek, This allows you to read from memory
# Poke, This allows you to write to memory

# Use ; as comments.

def getFile() -> str:
    while True:
        fileName = input("Enter the Bear program you would like to compile (with the extension): ")
        if fileName[-5:] != ".bear":
            print("The filename must have a .bear extension.")
            continue
        try:
            with open(f"Bear-16_CPU/Software/Bear/{fileName}", "r"):
                return fileName
        except FileNotFoundError:
            print("This file does not exist")
            continue

class decode:
    def __init__(self, fileName):
        self.fileName = fileName
        self.getLines()
        self.findVariables()

    def getLines(self):
        self.lines = []
        with open(f"Bear-16_CPU/Software/Bear/{self.fileName}", "r") as file:
            for line in file:
                line = line.replace('\n', '').strip()
                
                if ";" in line:
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
                            line = line[:indexJ].strip()
                            break
                if line != "":
                    self.lines.append(line)
            print(self.lines)

    def findVariables(self):
        self.variables = {}
    

def main():
    fileName = "fibbonachi.bear" # getFile()
    decode(fileName)

if __name__ == "__main__":
    main()