def fixBits(data: int, bits: int = 16) -> int:
    mask = (1 << bits) - 1
    return mask & data

# Registers
class register:
    def __init__(self, name: str, index: int, data: int = 0) -> None:
        self.name = name
        self.index = index
        self.data = fixBits(data)

    def store(self, data: int) -> None:
        self.data = fixBits(data)

    def read(self) -> int:
        return fixBits(self.data)

# Special registers: Stack Pointer, Memory Address Register, Program Counter, Memory Data Register, Current Instruction Register, Accumulator
class accumulator(register):
    def __init__(self) -> None:
        super().__init__("Accumulator", 7, 0)

    def add(self, register: object) -> None:
        self.data = fixBits(self.data + register.read())
    def sub(self, register: object) -> None:
        self.data = fixBits(self.data - register.read())
    def neg(self) -> None:
        self.data = fixBits(-self.data)
    def bitwiseAnd(self, register: object) -> None:
        self.data = fixBits(self.data & register.read())
    def bitwiseOr(self, register: object) -> None:
        self.data = fixBits(self.data | register.read())
    def bitwiseNot(self) -> None:
        self.data = fixBits(0xFFFF - fixBits(self.data))
    def bitwiseXor(self, register: object) -> None:
        self.data = fixBits(self.data ^ register.read())
    def leftShift(self) -> None:
        self.data = fixBits(fixBits(self.data) << 1)
    def rightShift(self) -> None:
        self.data = fixBits(fixBits(self.data) >> 1)

class stackPointer(register):
    def __init__(self, ram: list[int]) -> None:
        self.stackStart = 0x0100
        self.stackSize = 0x100

        super().__init__("Stack Pointer", 8, self.stackStart)

        self.ram = ram

    def push(self, data: int) -> None:
        self.ram[fixBits(self.data)] = fixBits(data)
        self.data = fixBits(self.data + 1)
        if self.data - self.stackStart >= self.stackSize:
            self.data = fixBits(self.stackStart)

    def pop(self) -> int:
        self.data = fixBits(self.data - 1)
        returnData = self.ram[fixBits(self.data)]

        if self.data < self.stackStart:
            print("?")
            self.data = fixBits(self.stackStart + self.stackSize - 1)

        return fixBits(returnData)

class MAR(register): # Memory Address Register
    def __init__(self, pc: object) -> None:
        super().__init__("Memory Address Register", 9, 0)

        self.pc = pc

    def store(self) -> None:
        self.data = fixBits(self.pc.read())

class PC(register): # Program Counter
    def __init__(self) -> None:
        pc_start = 0xC000
        super().__init__("Program Counter", 10, pc_start)

    def inc(self) -> None:
        self.data = fixBits(self.data + 1)

class MDR(register): # Memory Data Register
    def __init__(self, ram: list[int], mar: object) -> None:
        super().__init__("Memory Data Register", 11, 0)
        self.ram = ram
        self.mar = mar

    def store(self) -> None:
        self.data = self.ram[fixBits(self.mar.read())]

class CIR(register): # Current Instruction Register
    def __init__(self, mdr: object) -> None:
        super().__init__("Current Instruction Register", 12, 0)
        self.mdr = mdr

    def store(self) -> None:
        self.data = fixBits(self.mdr.read())

def main():
    print("Welcome to the Bear-16 CPU Emulator")

if __name__ == "__main__":
    main()