# noqa: N999
import Peripherals.keyboardInput as keyboardInput  # noqa: PLR0402
import Peripherals.secondaryMemory as secondaryMemory  # noqa: PLR0402
import Peripherals.terminal as terminal  # noqa: PLR0402


class peripheral:
    def __init__(self):
        self.peripherals = [
            terminal.terminal(0x6002, 0x6003),
            keyboardInput.keyboardInput(0x7000, 0x7100),
            secondaryMemory.secondaryMemory(0x6012, 0x6013, 0x6014, 0x6015, "Bear-16_CPU/Peripherals/secondaryMemory.bin"),
        ]

    def confirmFormat(self, searchAddress: int) -> str:
        format = ""
        for p in self.peripherals:
            addresses = p.addresses
            for address in addresses:
                if address == searchAddress:
                    format = p.addresses[address]
        return format

    def sendData(self, data, dataAddress: int) -> None:
        for p in self.peripherals:
            addresses = p.datas
            for address in addresses:
                if address == dataAddress:
                    p.sendData(data, dataAddress)
                    return

    def readData(self, dataAddress: int) -> int:
        for p in self.peripherals:
            addresses = p.datas
            for address in addresses:
                if address == dataAddress:
                    return p.readData(dataAddress)
        return 0x0000