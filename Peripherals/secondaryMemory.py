def fixBits(data: int, bits: int = 16) -> int: # noqa: N999
    mask = (1 << bits) - 1
    return mask & data

class secondaryMemory:
    def __init__(self, dataInAdd: int, dataOutAdd: int, addressAdd: int, clockAdd: int, fileName: str): 
        # Data In Add is the address of the data where it reads from, 
        # Data Out Add is the address of the data where it writes to, 
        # addressAdd is the address of the address in the storage where the data will be written to,
        # Clock add is the address of the clock,
        # fileName is the name of the data file ; Usually set to "Peripherals/secondaryMemory.bin"
        self.dataInAdd = dataInAdd
        self.dataOutAdd = dataOutAdd
        self.addressAdd = addressAdd
        self.clockAdd = clockAdd
        self.fileName = fileName

        self.addresses = {dataInAdd: "W", dataOutAdd: "R", addressAdd: "W", clockAdd: "W"} # Address book for this peripheral
        self.datas = {dataInAdd: 0, dataOutAdd: 0, addressAdd: 0, clockAdd: 0} # Data book for this peripheral

        try:
            with open(fileName, "r") as memory:
                if len(memory.read()) != 262144:
                    raise(FileNotFoundError)
        except FileNotFoundError:
            data = [0x0000] * 65536

            with open(fileName, "w") as memory:
                for word in data:
                    word = hex(word).replace('0x', '').zfill(4)
                    memory.write(word)

    def sendData(self, data: int, dataAdd: int) -> None:
        self.datas[dataAdd] = data
        self.execute()

    def readData(self, dataAdd: int) -> int:
        return self.datas[dataAdd]
    
    def execute(self) -> None:
        memoryData = []
        with open(self.fileName, "r") as memory:
            data = memory.read()
            for i in range(65536):
                word = ""
                for nibble in range(4):
                    word += data[i * 4 + nibble]
                word = int(word, 16)
                memoryData.append(hex(word).replace('0x', '').zfill(4))

        data = self.datas[self.dataInAdd]
        address = self.datas[self.addressAdd]

        if self.datas[self.clockAdd] != 0:
            with open(self.fileName, "w") as memory:
                data = hex(fixBits(data)).replace('0x', '').zfill(4)

                memoryData[address] = data

                for data in memoryData:
                    memory.write(data)

            self.datas[self.clockAdd] = 0

        self.datas[self.dataOutAdd] = int(memoryData[address], 16)