# BEAR-16 CPU

This is an emulator for a custom CPU
This project also holds the assembler and peripherals for this CPU



## INSTRUCTIONS:
These are the instructions you can use in the CPU.
The number is the machine code and the command afterwards is the Assembly command
0.  0x00 NOP
1.  0x01 LDR x y ; Loads y (Data bus) into register x (Condition bus)
2.  0x02 LDM x y ; Loads value at memory address y (Data bus) into register x (Condition bus)
3.  0x03 STM x y ; Loads value in register x (Condition bus) into memory address y (Data bus)
4.  0x04 *STM x y ; Loads value in register y (Data bus) into memory address x (Condition bus)
5.  0x05 ADD x ; Adds x (Data bus) to Accumulator
6.  0x06 ADDC x ; Adds x (Data bus) and Carry to Accumulator
7.  0x07 SUB x ; Subtracts x (Data bus) from Accumulator
8.  0x08 SUBC x ; Subtracts x (Data bus) and Carry from Accumulator
9.  0x09 NEG ; Negates the accumulator
10. 0x0A AND x ; ANDs x (Data bus) and Accumulator
11. 0x0B OR ; ORs x (Data bus) and Accumulator
12. 0x0C NOT ; NOTs the Accumulator
13. 0x0D XOR x ; XORs x (Data bus) and Accumulator
14. 0x0E LTS ; Left Shifts the Acc
15. 0x0F RTS ; Right Shifts the Acc
16. 0x10 JGT x y ; Jumps to y (Data bus) if x (Condition bus) is greater than 0
17. 0x11 JEQ x y ; Jumps to y (Data bus) if x (Condition bus) is equal to 0
18. 0x12 JGE x y ; Jumps to y (Data bus) if x (Condition bus) is greater than or equal to 0
19. 0x13 JLT x y ; Jumps to y (Data bus) if x (Condition bus) is less than 0
20. 0x14 JNE x y ; Jumps to y (Data bus) if x (Condition bus) is not equal to 0
21. 0x15 JLE x y ; Jumps to y (Data bus) if x (Condition bus) is less than or equal to 0
22. 0x16 *JGT x y ; Jumps to x (Condition bus) if y (Data bus) is greater than 0
23. 0x17 *JEQ x y ; Jumps to x (Condition bus) if y (Data bus) is equal to 0
24. 0x18 *JGE x y ; Jumps to x (Condition bus) if y (Data bus) is greater than or equal to 0
25. 0x19 *JLT x y ; Jumps to x (Condition bus) if y (Data bus) is less than 0
26. 0x1A *JNE x y ; Jumps to x (Condition bus) if y (Data bus) is not equal to 0
27. 0x1B *JLE x y ; Jumps to x (Condition bus) if y (Data bus) is less than or equal to 0
28. 0x1C JMP x ; Jumps to x (Data bus)
29. 0x1D PUSH x ; Pushes x (Data bus) to the stack
30. 0x1E POP x ; Pops from the stack and places in x (Condition bus)
31. 0x1F JSR x ; Pushes current address to stack then jumps to x (Data bus)
32. 0x20 RSR ; Pops return address from stack then jumps back to return address


## OPERANDS:
Operands are 8-bits
Bits A + B are the Data Type: 00 means Register, 01 means Immediate, 10 means Carry, 11 means PC
Bits C + D + E are the Condition bus: 000 means r0, 001 means r1, 010 means r2, 011 means r3, 100 means r4, 101 means r5, 110 means r6, 111 means Accumulator (This is shortened to racc in the assembler)
Bits F + G + H are the Data bus. It has the same codes as the Condition bus but if the Data Type isn't 00 then it the data bus is overridden by the data type

### Data Type hex codes:
0x00: Register
0x40: Immediate
0x80: Carry
0xC0: PC

### Condition Bus hex codes:
0x00: r0
0x08: r1
0x10: r2
0x18: r3
0x20: r4
0x28: r5
0x30: r6
0x38: acc

### Data Bus hex codes:
0x00: r0
0x01: r1
0x02: r2
0x03: r3
0x04: r4
0x05: r5
0x06: r6
0x07: acc





# BEAR-16 Assembler

## SPECIAL COMMANDS:
.zstring inserts a string of characters such as "Hello World!" as ascii codes into the memory with a zero at the end.
.org sets the placement address of the code that follows such as .org $8000 which makes the code that follows start at address $8000
.word inserts two bytes into the memory

## NUMBERS:
$ is a hex number
\% is a binary number
£ is an octary number
No symbol means it is a denary number

## COMMANDS, LABELS and CONSTANTS:
To differentiate code and commands, labels and constants you put spaces at the start
This is an instruction: "   LTS"
This is a label: "label:"


There are three things the assembler adds, Constants, Labels and Commands
These things require there to be no spaces at the start of the line
To define a constant you put the name then an equals sign then the number such as Pi = 3
To define a label you put the name then a colon such as label:
To use a command you put the command and if needed an input such as .zstring "Hello World!"


You can use constants in the place of immediates
You can define constants anywhere but it is recommended you only place them at the start


You can use .org anywhere but it is recommended you keep them in order such as .org $8000 is before .org $C000
You do have to ensure .org is at the start set to $8000 and you don't go below because that is where the ROM starts otherwise the code won't get decoded.


## COMMENTS:
To do comments you do a ; then everything after is a comment.
To do characters you do a pair of " or a pair of ' and the character inside will be replaced with the ascii code
You do the same with string as with characters


## SPECIAL CHARACTERS:
If you want to have a \ as just a character in zstrings you have to do 4 \ such as "\\\\"
In regular characters you have to do 2 \ such as "\\"

To do ESC in characters and zstrings you do \e





# PERIPHERALS
Peripherals are extra devices you can add to the CPU so you can have more functions.
Currently there are 3 pre-made devices: Terminal, Keyboard and Secondary Memory


## EDITING PERIPHERALS
The address of a peripheral is configurable inside Peripheral.py
This address has to be more than $3FFF and less than $8000


## NEW PERIPHERALS
These peripherals can be added multiple times due to the class structure of them allowing for more usage. For example you could add another secondary memory.
To add a new peripheral you just need to import the module where it is held and then create a class of it inside the list.


### REQUIREMENTS
#### In every peripheral you must have 4 things otherwise it will not work. These 4 things are:
A dictionary of the addresses and their condition (W for write, R for read, you can combine for both or leave out for neither) called addresses
A dictionary of the addresses and their data called datas
A function called "sendData" with the inputs of data and data address and output of None
A function called "readData" with the input of data address and output of the data


All inputs and outputs must be integers.

## USING PERIPHERALS
To use a peripheral you just need to reference it in the assembly code by grabbing data from and putting data into the addresses $4000 to $7FFF.