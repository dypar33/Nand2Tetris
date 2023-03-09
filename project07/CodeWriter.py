# class SegmentTable:
#     address_table = {
#         "local" : "",
#         "argument",
#         "pointer",
#         "this",
#         "that",
#         "static", [16, 255]
#     }

class CodeWriter:
    __comp_count = 0

    def __init__(self, filename):
        self.fd = open(filename+".asm", "w")

    def set_filename(self, filename):
        self.fd = open(filename+".asm", 'w')

    def write_arithmetics(self, command):
        handler = getattr(self, '_asm_' + command)

        asm = handler()

        self._write_asm_to_file(asm)

    def write_push_pop(self, command, segment, index):
        handler = getattr(self, '_asm_'+command)
        
        asm = handler(segment, index)

        self._write_asm_to_file(asm)

    def _write_asm_to_file(self, data):
        self.fd.write(data)


    def close(self):
        self.fd.close()

    def _asm_push(self, segment, index) -> str:
        """
            D=[push value]
            
            @SP
            A=M
            M=D
            
            @SP
            M=M+1
        """

        handler = getattr(self, "_segment_" + segment)

        asm = ""
        asm += handler(index)

        if segment != 'constant':
            asm += "D=M\n"
        asm += self.__access_stack_by_sp()
        asm += "M=D\n"
        asm += self.__inc_sp()

        return asm


    def _asm_pop(self, segment, index) -> str:
        """
            @[offset]
            D=A

            @[segment]
            A=M+D
            D=A

            @[various reg]
            M=D

            @SP
            M=M-1

            @SP
            A=M
            D=M

            @[various reg]
            A=M
            M=D
        """

        segment_handler = getattr(self, "_segment_" + segment)

        asm = ""
        asm += segment_handler(index)
        asm += "D=A\n"
        asm += self.__access_various_register(0)
        asm += "M=D\n"
        asm += self.__dec_sp()
        asm += self.__access_stack_by_sp()
        asm += "D=M\n"
        asm += self.__access_various_register(0)
        asm += "A=M\n"
        asm += "M=D\n"

        return asm

    def _asm_add(self) -> str:
        asm = self.__two_argu_arithmetics_template()

        return asm.format("+")
    
    def _asm_sub(self) -> str:
        asm = self.__two_argu_arithmetics_template()

        return asm.format("-")
    
    def _asm_and(self) -> str:
        asm = self.__two_argu_arithmetics_template()

        return asm.format("&")
    
    def _asm_or(self) -> str:
        asm = self.__two_argu_arithmetics_template()

        return asm.format("|")
    
    def _asm_eq(self) -> str:
        asm = self.__comp_template().format("JEQ")
        
        return asm

    def _asm_lt(self) -> str:
        asm = self.__comp_template().format("JLT")
        
        return asm

    def _asm_gt(self) -> str:
        asm = self.__comp_template().format("JGT")
        
        return asm
    
    def _asm_neg(self) -> str:
        asm = self.__one_argu_arithmetics_template().format("-")

        return asm
    
    def _asm_not(self) -> str:
        asm = self.__one_argu_arithmetics_template().format("!")

        return asm

    def _segment_constant(self, value):
        """
            @[value]
            D=A
        """

        return "@{}\nD=A\n".format(value)
    
    def _segment_argument(self, value):
        return self.__segment_template().format(value, "ARG")
    
    def _segment_local(self, value):
        return self.__segment_template().format(value, "LCL")
    
    def _segment_this(self, value):
        return self.__segment_template().format(value, "THIS")
    
    def _segment_that(self, value):
        return self.__segment_template().format(value, "THAT")
    
    def _segment_pointer(self, value):
        value = int(value)

        assert(value + 3 < 5)

        asm = "@R{}\n".format(value + 3)

        return asm
    
    def _segment_temp(self, value):
        value = int(value)

        assert(value + 5 < 13)

        asm = "@R{}\n".format(value + 5)

        return asm
    
    def _segment_static(self, value):
        asm = "@{}\nD=A\n".format(value)
        asm += "@16\n"                  # 16 is static mem address
        asm += "A=A+D\n"

        return asm
    
    def __segment_template(self) -> str:
        """
            @[value]
            D=A

            @[register]
            A=M+D
        """
        asm = "@{0}\nD=A\n"
        asm += "@{1}\n"
        asm += "A=M+D\n"

        return asm
        
    
    def __one_argu_arithmetics_template(self) -> str:
        """
            @SP
            A=M
            A=A-1
            M=[]M
        """
        asm = ""
        asm += self.__access_stack_by_sp()
        asm += self.__dec_a()
        asm += "M={}M\n"

        return asm 
    
    def __two_argu_arithmetics_template(self) -> str:
        """
            @SP
            M=M-1

            @SP
            A=M
            D=M

            @SP
            A=M
            A=A-1
            M=D[operator]M
        """

        asm = ""
        asm += self.__dec_sp()
        asm += self.__access_stack_by_sp()
        asm += "D=M\n"
        asm += self.__access_stack_by_sp()
        asm += self.__dec_a()
        asm += "M=M{}D\n"

        return asm
    
    def __comp_template(self) -> str:
        asm = self.__two_argu_arithmetics_template().format("-")

        # @SP
        # A=M
        # A=A-1
        # D=M
        # @TRUE
        # D; []
        asm += self.__access_stack_by_sp()
        asm += "A=A-1\n"
        asm += "D=M\n"
        asm += "@TRUE{}\n".format(self.__comp_count)
        asm += "D;{0}\n"

        # @SP
        # A=M
        # A=A-1
        # M=0
        # @END
        # 0;JMP
        asm += self.__access_stack_by_sp()
        asm += self.__dec_a()
        asm += "M=0\n"
        asm += "@END{}\n".format(self.__comp_count)
        asm += self.__jump()

        # @SP
        # A=A-1
        # M=-1
        asm += "(TRUE{})\n".format(self.__comp_count)
        asm += self.__access_stack_by_sp()
        asm += self.__dec_a()
        asm += "M=-1\n"

        asm += "(END{})\n".format(self.__comp_count)

        self.__comp_count += 1

        return asm

    def __access_stack_by_sp(self) -> str:
        """
            @SP
            A=M
        """
        return "@SP\nA=M\n"
    
    def __access_various_register(self, index) -> str:
        """
            @R13 + []
        """
        assert(index+13 < 16)

        return "@R{}\n".format(13 + index)
    
    def __jump(self) -> str:
        return "0; JMP\n"
    
    def __inc_sp(self) -> str:
        """
            @SP
            M=M+1
        """
        return "@SP\nM=M+1\n"
    
    def __dec_sp(self) -> str:
        """
            @SP
            M=M-1
        """
        return "@SP\nM=M-1\n"
    
    def __inc_a(self) -> str:
        return "A=A+1\n"
    
    def __dec_a(self) -> str:
        return "A=A-1\n"
    
    def __inc_m(self) -> str:
        return "M=M+1\n"
    
    def __dec_m(self) -> str:
        return "M=M-1\n"