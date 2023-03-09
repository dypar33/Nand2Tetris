import sys
import os

from Parser import Parser, CommandType
from SymbolTable import SymbolTable
from Code import Code
from Exception import *

class Assembler():

    def __init__(self, file_name):
        self.file_name = os.path.basename(file_name).split('.')[0]
        self.f =  open(file_name, 'r')
        self.parser = Parser(self.f)
        self.sym_table = SymbolTable()
        pass

    def assembly(self):
        self._first_phase()
        self._second_phase()

    def _first_phase(self):
        rom_number = 0
        
        while self.parser.advance():
            command_type = self.parser.command_type()
            
            if command_type == CommandType.L_COMMAND:
                symbol = self.parser.symbol()

                self.sym_table.add_entry(symbol, rom_number)

                continue
            elif command_type == CommandType.IGNORE:
                continue
            
            rom_number += 1
        
        self.parser.fd.seek(0)

    def _second_phase(self):
        line_number = -1
        with open(self.file_name + '.hack', 'w') as fw:
            while self.parser.advance():
                line_number += 1 # for debug 

                binary_code = ""
                command_type = self.parser.command_type()

                if command_type == CommandType.A_COMMAND:
                    symbol = self.parser.symbol()

                    
                    if symbol.isdigit():
                        address = int(symbol)
                    else:
                        if not self.sym_table.contains(symbol):
                            self.sym_table.add_entry(symbol)
                        
                        address = self.sym_table.get_address(symbol)

                    binary_code = Code.a_instrunction(address)

                elif command_type == CommandType.C_COMMAND:
                    binary_code = "111" + Code.comp(self.parser.comp()) + Code.dest(self.parser.dest()) + Code.jump(self.parser.jump())
                else:
                    continue
                
                binary_code += '\n'
                fw.write(binary_code)

 

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: assembler [target file path]")
        exit()

    assembler = Assembler(sys.argv[1])
    assembler.assembly()

