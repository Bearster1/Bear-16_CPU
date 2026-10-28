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

            self.cpu.peripheral.sendData(data, address) # type: ignore
            
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
        self.peripheral = Peripheral.peripheral()

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
        # operand will be a look up table: 
        #   Bits A + B = Data type, 00: Register, 01: Immediate, 10: Carry, 11: PC
        #   Bits C + D + E = Register 1 also called the condition bus: r0, r1, r2, r3, r4, r5, r6, acc (This is the register used for writing)
        #   Bits F + G + H = Register 2 also called the data bus: r0, r1, r2, r3, r4, r5, r6, acc (This is the register used for reading, it is replaced by data type)

        self.immediate = False
        data_type = self.operand >> 6
        match data_type:
            case 1:
                self.immediate = True
                self.data_bus = self.MDR
            case 2: self.data_bus = self.carry
            case 3: self.data_bus = self.PC
            case _:
                register2 = fixBits(self.operand, 3)
                match register2:
                    case 0: self.data_bus = self.r0
                    case 1: self.data_bus = self.r1
                    case 2: self.data_bus = self.r2
                    case 3: self.data_bus = self.r3
                    case 4: self.data_bus = self.r4
                    case 5: self.data_bus = self.r5
                    case 6: self.data_bus = self.r6
                    case 7: self.data_bus = self.acc

        register1 = fixBits(self.operand >> 3, 3)
        match register1:
            case 0: self.condition_bus = self.r0
            case 1: self.condition_bus = self.r1
            case 2: self.condition_bus = self.r2
            case 3: self.condition_bus = self.r3
            case 4: self.condition_bus = self.r4
            case 5: self.condition_bus = self.r5
            case 6: self.condition_bus = self.r6
            case 7: self.condition_bus = self.acc

    def execute(self) -> None:
        match self.opcode:
            case 0: return # NOP


            case 1: self.condition_bus.store(self.data_bus.read()) # LDR x y ; Loads y (Data bus) into register x (Condition bus)
            case 2: self.condition_bus.store(self.memory.read(self.data_bus.read())) # LDM x y ; Loads value at memory address y (Data bus) into register x (Condition bus)
            case 3: self.memory.store(self.condition_bus.read(), self.data_bus.read()) # STM x y ; Loads value in register x (Condition bus) into memory address y (Data bus)
            case 4: self.memory.store(self.data_bus.read(), self.condition_bus.read()) # STM x y ; Loads value in register x (Data bus) into memory address y (Condition bus) ; The name of this command is subject to change


            case 5: self.acc.add(self.data_bus) # ADD x ; Adds x (Data bus) to Accumulator
            case 6: self.acc.addc(self.data_bus) # ADDC x ; Adds x (Data bus) and Carry to Accumulator
            case 7: self.acc.sub(self.data_bus) # SUB x ; Subtracts x (Data bus) from Accumulator
            case 8: self.acc.subc(self.data_bus) # SUBC x ; Subtracts x (Data bus) and Carry from Accumulator
            case 9: self.acc.neg() # NEG ; Negates the accumulator
            case 10: self.acc.bitwiseAnd(self.data_bus) # AND x ; ANDs x (Data bus) and Accumulator
            case 11: self.acc.bitwiseOr(self.data_bus) # OR ; ORs x (Data bus) and Accumulator
            case 12: self.acc.bitwiseNot() # NOT ; NOTs the Accumulator
            case 13: self.acc.bitwiseXor(self.data_bus) # XOR ; XORs x (Data bus) and Accumulator
            case 14: self.acc.leftShift() # LTS ; Left Shifts the Acc
            case 15: self.acc.rightShift() # RTS ; Right Shifts the Acc


            case 16: # JGT x y ; Jumps to y (Data bus) if x (Condition bus) is greater than 0
                if self.condition_bus.read() > 0 and self.condition_bus.read() < 0x8000:
                    self.PC.store(self.data_bus.read())
            case 17: # JEQ x y ; Jumps to y (Data bus) if x (Condition bus) is equal to 0
                if self.condition_bus.read() == 0:
                    self.PC.store(self.data_bus.read())
            case 18: # JGE x y ; Jumps to y (Data bus) if x (Condition bus) is greater than or equal to 0
                if (self.condition_bus.read() > 0 and self.condition_bus.read() < 0x8000) or self.condition_bus.read() == 0:
                    self.PC.store(self.data_bus.read())
            case 19: # JLT x y ; Jumps to y (Data bus) if x (Condition bus) is less than 0
                if self.condition_bus.read() < 0x7FFF:
                    self.PC.store(self.data_bus.read())
            case 20: # JNE x y ; Jumps to y (Data bus) if x (Condition bus) is not equal to 0
                if self.condition_bus.read() != 0:
                    self.PC.store(self.data_bus.read())
            case 21: # JLE x y ; Jumps to y (Data bus) if x (Condition bus) is less than or equal to 0
                if self.condition_bus.read() < 0x7FFF or self.condition_bus.read() == 0:
                    self.PC.store(self.data_bus.read())

            case 22: # JGT x y ; Jumps to y (Condition bus) if x (Data bus) is greater than 0
                if self.data_bus.read() > 0 and self.data_bus.read() < 0x8000:
                    self.PC.store(self.condition_bus.read())
            case 23: # JEQ x y ; Jumps to y (Condition bus) if x (Data bus) is equal to 0
                if self.data_bus.read() == 0:
                    self.PC.store(self.condition_bus.read())
            case 24: # JGE x y ; Jumps to y (Condition bus) if x (Data bus) is greater than or equal to 0
                if (self.data_bus.read() > 0 and self.data_bus.read() < 0x8000) or self.data_bus.read() == 0:
                    self.PC.store(self.condition_bus.read())
            case 25: # JLT x y ; Jumps to y (Condition bus) if x (Data bus) is less than 0
                if self.data_bus.read() < 0x7FFF:
                    self.PC.store(self.condition_bus.read())
            case 26: # JNE x y ; Jumps to y (Condition bus) if x (Data bus) is not equal to 0
                if self.data_bus.read() != 0:
                    self.PC.store(self.condition_bus.read())
            case 27: # JLE x y ; Jumps to y (Condition bus) if x (Data bus) is less than or equal to 0
                if self.data_bus.read() < 0x7FFF or self.condition_bus.read() == 0:
                    self.PC.store(self.condition_bus.read())
            
            case 28: self.PC.store(self.data_bus.read()) # JMP x ; Jumps to y (Data bus)


            case 29: self.stackPointer.push(self.data_bus.read()) # PUSH x ; Pushes x (Data bus) to the stack
            case 30: self.condition_bus.store(self.stackPointer.pop()) # POP x ; Pops from the stack and places in x (Condition bus)
            case 31: # JSR x ; Pushes current address to stack then jumps to x (Data Bus)
                self.stackPointer.push(self.PC.read())
                self.PC.store(self.data_bus.read())
            case 32: # RSR ; Pops return address from stack then jumps back to return address
                self.PC.store(self.stackPointer.pop())

    def loadROM(self) -> None:
        with open("Bear-16_CPU/Software/Binary/ROM.bin", "r") as ROM:
            program = ROM.read()
            for i in range(32768):
                word = ""
                for nibble in range(4):
                    word += program[i * 4 + nibble]
                word = int(word, 16)
                self.memory.writeROM(word, i + 0x8000)

def main():
    print("Welcome to the Bear-16 CPU Emulator")

if __name__ == "__main__":
    main()