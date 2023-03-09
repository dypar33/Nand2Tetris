class SymbolTable:
    table = {
        "SP"     : 0,
        "LCL"    : 1,
        "ARG"    : 2,
        "THIS"   : 3,
        "THAT"   : 4,
        "R0"     : 0,
        "R1"     : 1,
        "R2"     : 2,
        "R3"     : 3,
        "R4"     : 4,
        "R5"     : 5,
        "R6"     : 6,
        "R7"     : 7,
        "R8"     : 8,
        "R9"     : 9,
        "R10"    : 10,
        "R11"    : 11,
        "R12"    : 12,
        "R13"    : 13,
        "R14"    : 14,
        "R15"    : 15,
        "SCREEN" : 16384,
        "KBD"    : 24576,
    }

    var_index = 16

    def __init__(self):
        pass

    def add_entry(self, symbol, address=-1):
        if address == -1:
            address = self.var_index
            self.var_index += 1

        self.table[symbol] = address

    def contains(self, symbol) -> bool:
        if symbol in self.table:
            return True
    
        return False

    def get_address(self, symbol) -> str:
        return self.table[symbol]