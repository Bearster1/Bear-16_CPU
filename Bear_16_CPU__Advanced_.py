import os
import time

import Bear_16_CPU as BearCPU
import Software.BBPL_Compiler as BBPLComp
import Software.Bear_16_Assembler as BearAsm
import Software.ROMWrite as ROMWrite  # noqa: PLR0402


def feature(message):
    print(f"You picked: {message}")
    time.sleep(2)
    os.system('cls')

print("Welcome to the Bear-16 CPU")
while True:
    print("""Select an option: 
    1) Use the Emulator
    2) Assemble a program
    3) Write the ROM
    4) Compile a BBPL program (WORK IN PROGRESS)
    5) Compile a Bear program (WORK IN PROGRESS - UNUSABLE)
    """)
    option = input()
    match option:
        case "1":
            feature("Emulate")
            BearCPU.main()
        case "2":
            feature("Assemble")
            BearAsm.main()
        case "3":
            feature("ROMWrite")
            ROMWrite.main()
        
        case "4":
            feature("Compile BBPL")
            BBPLComp.main()
        case _:
            print("This is not an option. Closing...")
            time.sleep(2)
            os.system('cls')
            break
    print("Option finished!")
    time.sleep(2)
    os.system('cls')
print("Thank you for using the Bear-16 CPU!")