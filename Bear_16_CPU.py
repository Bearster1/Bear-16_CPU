import Peripherals.Peripheral as Peripheral  # noqa: PLR0402


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
class carry(register):
    def __init__(self) -> None:
        super().__init__("Carry", 7, 0)

class accumulator(register):
    def __init__(self, carry: object) -> None:
        super().__init__("Accumulator", 8, 0)
        self.carry = carry

    def accFixBits(self, data: int, bits: int = 16):
        strdata = bin(data).replace("0b", "").replace("-", "")
        if len(strdata) >= bits + 1:
            self.carry.store(fixBits(int(strdata[len(strdata) - (bits + 1)]))) # type: ignore
        else:
            self.carry.store(0) # type: ignore
        return fixBits(data, bits)

    def add(self, register: object) -> None:
        self.data = self.accFixBits(self.data + register.read()) # type: ignore
    def addc(self, register: object) -> None:
        self.data = self.accFixBits(self.data + register.read() + self.carry.read()) # type: ignore
    def sub(self, register: object) -> None:
        result = self.data - register.read() # type: ignore
        if self.data >= register.read(): # type: ignore
            result += 0x10000
        self.data = self.accFixBits(result)
    def subc(self, register: object) -> None:
        result = self.data - register.read() - self.carry.read() # type: ignore
        if (self.data >= register.read() and self.carry.read() == 0) or (self.data > register.read() and self.carry.read() == 1): # type: ignore
            result += 0x10000
        self.data = self.accFixBits(result)
    def neg(self) -> None:
        self.data = self.accFixBits(-self.data)
    def bitwiseAnd(self, register: object) -> None:
        self.data = self.accFixBits(self.data & register.read()) # type: ignore
    def bitwiseOr(self, register: object) -> None:
        self.data = self.accFixBits(self.data | register.read()) # type: ignore
    def bitwiseNot(self) -> None:
        self.data = self.accFixBits(0xFFFF - fixBits(self.data))
    def bitwiseXor(self, register: object) -> None:
        self.data = self.accFixBits(self.data ^ register.read()) # type: ignore
    def leftShift(self) -> None:
        self.data = self.accFixBits(fixBits(self.data) << 1)
    def rightShift(self) -> None:
        self.data = self.accFixBits(fixBits(self.data) >> 1)

class stackPointer(register):
    def __init__(self, mem: object) -> None:
        self.stackStart = 0x0100
        self.stackSize = 0x100

        super().__init__("Stack Pointer", 9, self.stackStart)

        self.mem = mem

    def push(self, data: int) -> None:
        self.mem.store(fixBits(data), fixBits(self.data)) # type: ignore
        self.data = fixBits(self.data + 1)
        if self.data - self.stackStart >= self.stackSize:
            self.data = fixBits(self.stackStart)

    def pop(self) -> int:
        self.data = fixBits(self.data - 1)
        returnData = self.mem.read(fixBits(self.data)) # type: ignore

        if self.data < self.stackStart:
            print("?")
            self.data = fixBits(self.stackStart + self.stackSize - 1)

        return fixBits(returnData)

class PC(register): # Program Counter
    def __init__(self) -> None:
        pc_start = 0x8000
        super().__init__("Program Counter", 10, pc_start)

    def inc(self) -> None:
        self.data = fixBits(self.data + 1)

class MAR(register): # Memory Address Register
    def __init__(self, pc: object) -> None:
        super().__init__("Memory Address Register", 11, 0)

        self.pc = pc

    def store(self) -> None: # type: ignore
        self.data = fixBits(self.pc.read()) # type: ignore

class MDR(register): # Memory Data Register
    def __init__(self, mem: object, mar: object) -> None:
        super().__init__("Memory Data Register", 12, 0)
        self.mem = mem
        self.mar = mar

    def store(self) -> None: # type: ignore
        self.data = self.mem.read(fixBits(self.mar.read())) # type: ignore

class CIR(register): # Current Instruction Register
    def __init__(self, mdr: object) -> None:
        super().__init__("Current Instruction Register", 13, 0)
        self.mdr = mdr

    def store(self) -> None: # type: ignore
        self.data = fixBits(self.mdr.read()) # type: ignore

# Memory
class memory:
    def __init__(self, cpu: object):
        # memory settup:
        # 0x0000 - 0x3FFF RAM
        # 0x4000 - 0x7FFF Peripherals
        # 0x8000 - 0xFFFF ROM
        self.name = "Memory"
        self.data = [0] * 65536
        self.cpu = cpu

    def writeROM(self, data: int, address: int) -> None:
        address = fixBits(address)
        data = fixBits(data)

        if address > 0x7FFF:
            self.data[address] = data

    def store(self, data: int, address: int) -> None:
        address = fixBits(address)
        data = fixBits(data)

        if address > 0x7FFF:
            return # Stops you from writing to the ROM
        elif address > 0x3FFF:
            format: str = self.cpu.peripheral.confirmFormat(address) # Returns R, W, RW or "" depending on if it can be read from, written to, both written to and read from or neither (If the address doesn't exist as a peripheral) # type: ignore
            if "W" not in format:
                return # Stops you from writing to Read-Only formats
            # Otherwise continues and writes to ram
            
        self.data[address] = data

    def read(self, address: int) -> int:
        address = fixBits(address)

        if address > 0x3FFF and address < 0x8000:
            format: str = self.cpu.peripheral.confirmFormat(address) # Returns R, W, RW or "" depending on if it can be read from, written to, both written to and read from or neither (If the address doesn't exist as a peripheral) # type: ignore
            if "R" not in format:
                return 0

        return self.data[address]

# CPU
class CPU:
    def __init__(self):
        self.peripheral = Peripheral.peripheral(self)

        #   Define Registers and Memory
        self.memory = memory(self)
        
        self.r0 = register("r0", 0, 0)
        self.r1 = register("r1", 1, 0)
        self.r2 = register("r2", 2, 0)
        self.r3 = register("r3", 3, 0)
        self.r4 = register("r4", 4, 0)
        self.r5 = register("r5", 5, 0)
        self.r6 = register("r6", 6, 0)

        self.carry = carry()
        self.acc = accumulator(self.carry)

        self.stackPointer = stackPointer(self.memory)
        self.PC = PC()
        self.MAR = MAR(self.PC)
        self.MDR = MDR(self.memory, self.MAR)
        self.CIR = CIR(self.MDR)

    def fetch(self) -> None:
        self.MAR.store()
        self.PC.inc()
        self.MDR.store()
        self.CIR.store()

        self.decode()
        if self.immediate:
            self.MAR.store()
            self.PC.inc()
            self.MDR.store()
        
    def decode(self) -> None:
        instruction = self.CIR.read()
        self.opcode = instruction >> 8
        self.operand = fixBits(instruction, 8)

        # opcode will be decoded through numbers
        # operand will be a look up table: Bits A + B = Data type, 00: Register, 01: Immediate, 10: Carry, 11: PC

        self.immediate = False # Temp variable to not cause crashes during testing

    def execute(self) -> None:
        pass # Implement later

def main():
    print("Welcome to the Bear-16 CPU Emulator")

if __name__ == "__main__":
    main()