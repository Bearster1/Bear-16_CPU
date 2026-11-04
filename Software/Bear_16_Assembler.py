import shlex  # noqa: N999

# This is the Bear-16 Assembler

# There will be commands you can use such as .zstring, .org, .word
# .zstring inserts a string of characters such as "Hello World!" as ascii codes into the memory with a zero at the end.
# .org sets the placement address of the code that follows such as .org $8000 which makes the code that follows start at address $8000
# .word inserts two bytes into the memory

# To specify which base the numbers are using you use different symbols such as $, %, £, and No symbol
# $ is a hex number
# % is a binary number
# £ is an octary number
# No symbol means it is a denary number

# To differentiate code and commands/ labels and constants you put spaces at the start
# This is an instruction: "   LTS"
# This is a label: "label:"

# There are three things the assembler adds, Constants, Labels and Commands
# These things require there to be no spaces at the start of the line
# To define a constant you put the name then an equals sign then the number such as Pi = 3
# To define a label you put the name then a colon such as label:
# To use a command you put the command and if needed an input such as .zstring "Hello World!"

# You can use constants in the place of immediates
# You can define constants anywhere but it is recommended you only place them at the start
# You can use .org anywhere but it is recommended you keep them in order such as .org $8000 is before .org $C000
# You do have to ensure .org is at the start set to $8000 and you don't go below because that is where the ROM starts otherwise the code won't get decoded.

# To do comments you do a ; then everything after is a comment.
# To do characters you do a pair of " or a pair of ' and the character inside will be replaced with the ascii code
# You do the same with string as with characters

# If you want to have a \ as just a character in zstrings you have to do 4 \ such as "\\\\"
# In regular characters you have to do 2 \ such as "\\"

# To do ESC in characters and zstrings you do \e

def base(number: str) -> int:
    number = number.strip()
    if number[0] == "$":
        # Hex

        number = number[1:]
        value = int(number, 16)
    elif number[0] == "%":
        # Bin
        
        number = number[1:]
        value = int(number, 2)
    elif number[0] == "£":
        # Oct

        number = number[1:]
        value = int(number, 8)
    else:
        # Den
        value = int(number)
    return value

def fixBits(data: int, bits: int = 16) -> int:
    mask = (1 << bits) - 1
    return mask & data

def decode(instruction: str, labels: dict, consts: dict) -> (int, int) | (int, None): # type: ignore
    parts = shlex.split(instruction.strip(), posix=False) # Splits but protects the space in the quotes
    opcode = parts[0].upper()
    data_bus = "NONE"
    condition_bus = "NONE"
    immediate = None

    operand = 0x00

    if opcode != "POP":
        if len(parts) > 1:
            data_bus = parts[-1]
        if len(parts) > 2:
            condition_bus = parts[1]
    else:
        condition_bus = parts[-1]

    data_type = 0x00
    if data_bus.lower() in ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "acc"]:
        data_type = 0x00
        match data_bus.lower():
            case "r0":  operand += 0x00
            case "r1":  operand += 0x01
            case "r2":  operand += 0x02
            case "r3":  operand += 0x03
            case "r4":  operand += 0x04
            case "r5":  operand += 0x05
            case "r6":  operand += 0x06
            case "acc": operand += 0x07
    elif data_bus.lower() == "carry":
        data_type = 0x80
    elif data_bus.lower() == "pc":
        data_type = 0xC0
    elif data_bus != "NONE":
        data_type = 0x40
        if data_bus in labels:
            immediate = labels[data_bus]
        elif data_bus in consts:
            immediate = consts[data_bus]
        elif "'" in data_bus or '"' in data_bus:
            char = shlex.split(data_bus)[0]
            if char == '\\n':
                immediate = 10
            elif char == '\\e':
                immediate = 27
            else:
                immediate = ord(char)
        else:
            immediate = base(data_bus)
    operand += data_type

    match condition_bus.lower():
        case "r0":  operand += 0x00
        case "r1":  operand += 0x08
        case "r2":  operand += 0x10
        case "r3":  operand += 0x18
        case "r4":  operand += 0x20
        case "r5":  operand += 0x28
        case "r6":  operand += 0x30
        case "acc": operand += 0x38

    match opcode:
        case "NOP":  opcode = 0x00
        case "LDR":  opcode = 0x01
        case "LDM":  opcode = 0x02
        case "STM":  opcode = 0x03
        case "*STM": opcode = 0x04
        case "ADD":  opcode = 0x05
        case "ADDC": opcode = 0x06
        case "SUB":  opcode = 0x07
        case "SUBC": opcode = 0x08
        case "NEG":  opcode = 0x09
        case "AND":  opcode = 0x0A
        case "OR":   opcode = 0x0B
        case "NOT":  opcode = 0x0C
        case "XOR":  opcode = 0x0D
        case "LTS":  opcode = 0x0E
        case "RTS":  opcode = 0x0F
        case "JGT":  opcode = 0x10
        case "JEQ":  opcode = 0x11
        case "JGE":  opcode = 0x12
        case "JLT":  opcode = 0x13
        case "JNE":  opcode = 0x14
        case "JLE":  opcode = 0x15
        case "*JGT": opcode = 0x16
        case "*JEQ": opcode = 0x17
        case "*JGE": opcode = 0x18
        case "*JLT": opcode = 0x19
        case "*JNE": opcode = 0x1A
        case "*JLE": opcode = 0x1B
        case "JMP":  opcode = 0x1C
        case "PUSH": opcode = 0x1D
        case "POP":  opcode = 0x1E
        case "JSR":  opcode = 0x1F
        case "RSR":  opcode = 0x20
        case _: opcode = 0x00

    code = (opcode << 8) + operand

    return code, immediate

    


def cleanse(instructions: list[str]) -> list[int]:
    cleanInstructions = []
    labels = {}
    consts = {}
    lineNum = 0
    for index in range(len(instructions)):
        instruction = instructions[index]
        if ';' in instruction:
            quote1 = False
            quote2 = False
            for indexJ in range(len(instruction)):
                character = instruction[indexJ]
                if character == "'":
                    quote1 = not quote1
                elif quote1:
                    continue
                if character == '"':
                    quote2 = not quote2
                elif quote2:
                    continue

                if character == ";":
                    instruction = instruction[:indexJ]
                    break

        if instruction.strip() == "":
            continue

        if instruction[0] == " ":
            pass
        else:
            if instruction[-1] == ":":
                # This is a label
                pass
            elif instruction[0] == ".":
                # This is a command
                pass
            elif "=" in instruction:
                # This is a const
                parts = instruction.strip().split('=')
                consts[parts[0].strip()] = base(parts[1])

                continue

        cleanInstructions.append(instruction)

    nonImmediates = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "acc", "carry", "pc"]

    lineNumInstructions = []
    for index in range(len(cleanInstructions)):
        instruction = cleanInstructions[index]

        if ".org" in instruction:
            lineNum = base(instruction.split(" ")[-1])
        elif ".zstring" in instruction:
            lineNum += len(instruction.split(" ")) + 1
        elif ".word" in instruction:
            lineNum += 1

        if lineNum < 0x8000:
            continue

        if instruction[0] == " ":
            parts = instruction.strip().split(" ")
            dataBus = parts[-1].lower()
            
            if dataBus not in nonImmediates and len(parts) > 1:
                lineNum += 1
            lineNum += 1
        elif instruction.strip()[-1] == ":":
            # Label
            name = instruction.strip()[:-1].strip()
            labels[name] = lineNum
            continue

        lineNumInstructions.append(instruction)

    decodedInstructions = [0x0000] * 32768
    lineNum = 0x0000
    for index in range(len(lineNumInstructions)):
        instruction = lineNumInstructions[index]

        if ".org" in instruction:
            lineNum = base(instruction.split(" ")[-1])
        elif ".zstring" in instruction:
            string = shlex.split(instruction)[-1]
            slash = False
            for character in string:
                if character == "\\" and not slash:
                    slash = not slash
                    continue
                elif character == "n" and slash:
                    character = 10
                elif character == "e" and slash:
                    character = 27
                else:
                    character = ord(character)
                decodedInstructions[lineNum - 0x8000] = fixBits(character)
                lineNum += 1
                slash = False
            decodedInstructions[lineNum - 0x8000] = 0x0000
            lineNum += 1
        elif ".word" in instruction:
            word = instruction.strip().split(" ")[-1]
            decodedInstructions[lineNum - 0x8000] = base(word)
            lineNum += 1

        else:
            decoded, immediate = decode(instruction, labels, consts)
            decodedInstructions[lineNum - 0x8000] = fixBits(decoded)
            lineNum += 1
            if immediate != None:
                decodedInstructions[lineNum - 0x8000] = fixBits(immediate)
                lineNum += 1
    return decodedInstructions    

def loadFile() -> list[str]:
    instructions = []
    with open("Bear-16_CPU/Software/Assembly/ROM.asm", "r") as ROM:
        for line in ROM:
            instructions.append(line.replace('\n', ''))
    return instructions

def writeFile(instructions: list[int]):
    with open("Bear-16_CPU/Software/Binary/ROM.bin", "w") as ROM:
        for word in instructions:
            word = hex(word).replace('0x', '').zfill(4)
            ROM.write(word)

def main():
    print("Welcome to the Bear-16 Assembler")
    instructions = loadFile()
    program = cleanse(instructions)
    writeFile(program)

    print("Complete")

if __name__ == "__main__":
    main()