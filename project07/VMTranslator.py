from CodeWriter import CodeWriter
from Parser import Parser, CommandType

import sys
import os

class VMTranslator():

    def __init__(self, file_name):
        self.file_name = os.path.basename(file_name).split('.')[0]
        self.f =  open(file_name, 'r')
        self.parser = Parser(self.f)
        self.code_writer = CodeWriter(self.file_name)

    def translate(self):
        self._first_phase()
        self._second_phase()

    def _first_phase(self):
        rom_number = 0
        
        while self.parser.advance():
            command_type = self.parser.command_type()
            
            if command_type == CommandType.C_ARITHMETIC:
                self.code_writer.write_arithmetics(self.parser.arg1())

                continue
            elif command_type == CommandType.C_PUSH or command_type == CommandType.C_POP:
                command = self.parser.arg1()
                argu = self.parser.arg2()

                self.code_writer.write_push_pop(command, *argu.split(' '))
            elif command_type == CommandType.C_IGNORE:
                continue
            
            rom_number += 1
        
        self.parser.fd.seek(0)

    def _second_phase(self):
        pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: VMTranslator.py [target file or directory]")

    target_file_list = []

    if os.path.isdir(sys.argv[1]):
        for file_name in os.listdir(sys.argv[1]):
            if file_name.endswith(".vm"):
                target_file_list.append(file_name)
    else:
        target_file_list.append(sys.argv[1])
        print(sys.argv[1])

    translator = VMTranslator(target_file_list[0])
    translator.translate()
    