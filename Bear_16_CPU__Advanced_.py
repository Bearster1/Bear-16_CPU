import os
import time

import Bear_16_CPU as BearCPU
import Software.Bear_16_Assembler as BearAsm


def feature(message):
    print(f"You picked: {message}")
    time.sleep(2)
    os.system('cls')

print("Welcome to the Bear-16 CPU")
print("""Select an option: 
1) Use the Emulator
2) Assemble a program
""")
option = input()
match option:
    case "1":
        feature("Emulate")
        BearCPU.main()
    case "2":
        feature("Assemble")
        BearAsm.main()
    case _:
        print("This is not an option. Closing...")
print("Option finished!")
time.sleep(2)
os.system('cls')
print("Thank you for using the Bear-16 CPU!")