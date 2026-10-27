def fixBits(data: int, bits: int = 16) -> int: # noqa: N999
    mask = (1 << bits) - 1
    return mask & data

def writeROM():
    program = [0x0000] * 32768

    words = [
        0x0140, # LDR r0 i1234
        0x1234,
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