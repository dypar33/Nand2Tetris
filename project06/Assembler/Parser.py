import enum

from Exception import *

class CommandType(enum.Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2
    IGNORE = 3


class Parser():
    def __init__(self, fd):
        self.fd = fd

        self.current_instruction = ""
        pass

    def advance(self) -> bool:
        instructions = self.fd.readline()

        if instructions == '':
            return False
        
        if '//' in instructions:
            instructions = instructions.split('//')[0]
        
        self.current_instruction = instructions.strip()
        
        return True

    def command_type(self) -> CommandType:
        if self.current_instruction.startswith("@"):
            return CommandType.A_COMMAND
        elif self.current_instruction.startswith("("):
            return CommandType.L_COMMAND
        elif self.current_instruction.startswith("//") or len(self.current_instruction) == 0:
            return CommandType.IGNORE
        else:
            return CommandType.C_COMMAND

    def symbol(self) -> str:
        if self.current_instruction.startswith('(') and self.current_instruction.endswith(')'):
            return self.current_instruction[1:-1]
        elif self.current_instruction.startswith('@'):
            return self.current_instruction[1:]
        else:
            raise SyntaxError

    def dest(self) -> str:
        if '=' in self.current_instruction:
            return self.current_instruction.split('=')[0]
        else:
            return ""

    def comp(self) -> str:
        if '=' in self.current_instruction:
            return self.current_instruction.split('=')[1]
        elif ';' in self.current_instruction:
            return self.current_instruction.split(';')[0]
        else:
            raise SyntaxError

    def jump(self) -> str:
        if ';' in self.current_instruction:
            return self.current_instruction.split(';')[1]
        else:
            return ""