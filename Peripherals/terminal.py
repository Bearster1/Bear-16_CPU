import manyterm


class terminal:
    def __init__(self, dataAdd: int, clockAdd: int) -> None: # Data Add is the address of the data and Clock add is the address of the clock
        self.dataAdd = dataAdd
        self.clockAdd = clockAdd

        self.addresses = {dataAdd: "W", clockAdd: "W"} # Address book for this peripheral
        self.datas = {dataAdd: 0, clockAdd: 0} # Data book for this peripheral

        self.terminal = manyterm.Terminal()

    def sendData(self, data: int, dataAdd: int) -> None:
        self.datas[dataAdd] = data
        self.execute()

    def readData(self, dataAdd: int) -> int:
        return 0x0000

    def execute(self) -> None:
        if self.datas[self.clockAdd] != 0:
            output = chr(self.datas[self.dataAdd])
            self.terminal.print(output, end="")
            self.datas[self.clockAdd] = 0