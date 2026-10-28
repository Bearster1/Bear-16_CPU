def fixBits(data: int, bits: int = 16) -> int: # noqa: N999
    mask = (1 << bits) - 1
    return mask & data

def writeROM():
    program = [0x0000] * 32768

    words = [
        # Make Hello World! print on a terminal
        # Terminal Data input is 0x6002
        # Terminal Clock input it 0x6003
        # Hello World! in hex is: 48 65 6C 6C 6F 20 57 6F 72 6C 64 21
        0x0140, # LDR r0 i6002
        0x6002,
        0x0148, # LDR r1 i6003
        0x6003,

        0x0440, # STM CHARACTER r0
        0x0048,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x0065,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x006C,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x006C,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x006F,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x0020,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x0057,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x006F,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x0072,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x006C,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x0064,
        0x0448, # STM i0001 r1
        0x0001,
        0x0440, # STM CHARACTER r0
        0x0021,
        0x0448, # STM i0001 r1
        0x0001,
        0x1C40, # JMP i803C
        0x8033
    ]

    for index in range(len(words)):
        program[index] = fixBits(words[index])

    with open("Bear-16_CPU/Software/Binary/ROM.bin", "w") as ROM:
        for word in program:
            word = hex(word).replace('0x', '').zfill(4)
            ROM.write(word)

def main():
    print("Welcome to the Bear-16 ROM Writer")
    writeROM()

if __name__ == "__main__":
    main()