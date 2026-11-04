import keyboard  # noqa: N999


class keyboardInput:
    def __init__(self, dataStartAdd: int, dataEndAdd: int) -> None: # Data Start Add is the address of the start of the data and Data End Add is the address of the end of the data
        self.dataStartAdd = dataStartAdd
        self.dataEndAdd = dataEndAdd

        self.addresses = {} # Address book for this peripheral
        self.datas = {} # Data book for this peripheral
        self.keyPointer = dataStartAdd
        
        for address in range(dataStartAdd, dataEndAdd):
            self.addresses[address] = "R"
            self.datas[address] = 0x0000

        keyboard.on_press(self.execute)

    def sendData(self, data: int, dataAdd: int) -> None:
        return

    def readData(self, dataAdd: int) -> int:
        return self.datas[dataAdd]

    def execute(self, pressedKey: object) -> None:
        keyName = pressedKey.name.lower() # type: ignore
        match keyName:
            case "esc": key = 0x0001
            case "f1": key = 0x0002
            case "f2": key = 0x0003
            case "f3": key = 0x0004
            case "f4": key = 0x0005
            case "f5": key = 0x0006
            case "f6": key = 0x0007
            case "f7": key = 0x0008
            case "f8": key = 0x0009
            case "f9": key = 0x000A
            case "f10": key = 0x000B
            case "f11": key = 0x000C
            case "f12": key = 0x000D
            case "print screen": key = 0x000E
            case "scroll lock": key = 0x000F
            case "pause": key = 0x0010
            case "insert": key = 0x0011
            case "home": key = 0x0012
            case "page up": key = 0x0013
            case "delete": key = 0x0014
            case "end": key = 0x0015
            case "page down": key = 0x0016
            case "num lock": key = 0x0017
            case "left": key = 0x0018
            case "right": key = 0x0019
            case "up": key = 0x001A
            case "down": key = 0x001B
            case "`": key = 0x001C
            case "1": key = 0x001D
            case "2": key = 0x001E
            case "3": key = 0x001F
            case "4": key = 0x0020
            case "5": key = 0x0021
            case "6": key = 0x0022
            case "7": key = 0x0023
            case "8": key = 0x0024
            case "9": key = 0x0025
            case "0": key = 0x0026
            case "-": key = 0x0027
            case "=": key = 0x0028
            case "backspace": key = 0x0029
            case "tab": key = 0x002A
            case "a": key = 0x002B
            case "b": key = 0x002C
            case "c": key = 0x002D
            case "d": key = 0x002E
            case "e": key = 0x002F
            case "f": key = 0x0030
            case "g": key = 0x0031
            case "h": key = 0x0032
            case "i": key = 0x0033
            case "j": key = 0x0034
            case "k": key = 0x0035
            case "l": key = 0x0036
            case "m": key = 0x0037
            case "n": key = 0x0038
            case "o": key = 0x0039
            case "p": key = 0x003A
            case "q": key = 0x003B
            case "r": key = 0x003C
            case "s": key = 0x003D
            case "t": key = 0x003E
            case "u": key = 0x003F
            case "v": key = 0x0040
            case "w": key = 0x0041
            case "x": key = 0x0042
            case "y": key = 0x0043
            case "z": key = 0x0044
            case "[": key = 0x0045
            case "]": key = 0x0046
            case "caps lock": key = 0x0047
            case "shift": key = 0x0048
            case "enter": key = 0x0049
            case "ctrl": key = 0x004A
            case "left windows": key = 0x004B
            case "right shift": key = 0x004C
            case "alt": key = 0x004D
            case "space": key = 0x004E
            case "menu": key = 0x004F
            case "right ctrl": key = 0x0050
            case ";": key = 0x0051
            case "'": key = 0x0052
            case "#": key = 0x0053
            case "\\": key = 0x0054
            case ",": key = 0x0055
            case ".": key = 0x0056
            case "/": key = 0x0057
            case "*": key = 0x0058
            case "+": key = 0x0059
            case "decimal": key = 0x005A
            case _: key = 0x0000

        self.datas[self.keyPointer] = key
        self.keyPointer += 1

        if self.keyPointer >= self.dataEndAdd:
            self.keyPointer = self.dataStartAdd
            for address in range(self.dataStartAdd, self.dataEndAdd):
                self.datas[address] = 0x0000