# BEAR-16 CPU

This is an emulator for a custom CPU
This project also holds the assembler and peripherals for this CPU



## INSTRUCTIONS:
These are the instructions you can use in the CPU.
The number is the machine code and the command afterwards is the Assembly command
0. NOP
1. LDR x y ; Loads y (Data bus) into register x (Condition bus)
2. LDM x y ; Loads value at memory address y (Data bus) into register x (Condition bus)
3. STM x y ; Loads value in register x (Condition bus) into memory address y (Data bus)
4. STM x y ; Loads value in register x (Data bus) into memory address y (Condition bus) ; The name of this command is subject to change
5. ADD x ; Adds x (Data bus) to Accumulator
6. ADDC x ; Adds x (Data bus) and Carry to Accumulator
7. SUB x ; Subtracts x (Data bus) from Accumulator
8. SUBC x ; Subtracts x (Data bus) and Carry from Accumulator
9. NEG ; Negates the accumulator
10. AND x ; ANDs x (Data bus) and Accumulator
11. OR ; ORs x (Data bus) and Accumulator
12. NOT ; NOTs the Accumulator
13. XOR ; XORs x (Data bus) and Accumulator
14. LTS ; Left Shifts the Acc
15. RTS ; Right Shifts the Acc
16. JGT x y ; Jumps to y (Data bus) if x (Condition bus) is greater than 0
17. JEQ x y ; Jumps to y (Data bus) if x (Condition bus) is equal to 0
18. JGE x y ; Jumps to y (Data bus) if x (Condition bus) is greater than or equal to 0
19. JLT x y ; Jumps to y (Data bus) if x (Condition bus) is less than 0
20. JNE x y ; Jumps to y (Data bus) if x (Condition bus) is not equal to 0
21. JLE x y ; Jumps to y (Data bus) if x (Condition bus) is less than or equal to 0
22. JGT x y ; Jumps to y (Condition bus) if x (Data bus) is greater than 0
23. JEQ x y ; Jumps to y (Condition bus) if x (Data bus) is equal to 0
24. JGE x y ; Jumps to y (Condition bus) if x (Data bus) is greater than or equal to 0
25. JLT x y ; Jumps to y (Condition bus) if x (Data bus) is less than 0
26. JNE x y ; Jumps to y (Condition bus) if x (Data bus) is not equal to 0
27. JLE x y ; Jumps to y (Condition bus) if x (Data bus) is less than or equal to 0
28. JMP x ; Jumps to x (Data bus)
29. PUSH x ; Pushes x (Data bus) to the stack
30. POP x ; Pops from the stack and places in x (Condition bus)
31. JSR x ; Pushes current address to stack then jumps to x (Data bus)
32. RSR ; Pops return address from stack then jumps back to return address


## OPERANDS:
Operands are 8-bits
Bits A + B are the Data Type: 00 means Register, 01 means Immediate, 10 means Carry, 11 means PC
Bits C + D + E are the Condition bus: 000 means r0, 001 means r1, 010 means r2, 011 means r3, 100 means r4, 101 means r5, 110 means r6, 111 means Accumulator (This is shortened to racc in the assembler)
Bits F + G + H are the Data bus. It has the same codes as the Condition bus but if the Data Type isn't 00 then it the data bus is overridden by the data type