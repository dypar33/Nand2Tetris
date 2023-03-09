import enum

class CommandType(enum.Enum):
    C_ARITHMETIC = 0
    C_PUSH       = 1
    C_POP        = 2
    C_LABEL      = 3
    C_GOTO       = 4
    C_IF         = 5
    C_FUNCTION   = 6
    C_RETURN     = 7
    C_CALL       = 8
    C_IGNORE     = 9

class CommandTable:
    ARITHMETIC_CMD = [
        "add", "sub", "neg", "and", "or", "not", "eq", "gt", "lt"
    ]


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
        command = self.current_instruction.split(' ')[0]

        if command == 'push':
            return CommandType.C_PUSH
        elif command == 'pop':
            return CommandType.C_POP
        elif command == 'goto':
            return CommandType.C_GOTO
        elif command.startswith('if'):
            return CommandType.C_GOTO
        elif command.startswith('//'):
            return CommandType.C_IGNORE
        elif command in CommandTable.ARITHMETIC_CMD:
            return CommandType.C_ARITHMETIC

    def arg1(self) -> str:
        return self.current_instruction.split(' ')[0]

    def arg2(self) -> int:
        return " ".join(self.current_instruction.split(' ')[1:])