
class Code:
    _dest_bin_code_table = {
        "" : "000",
        "null" : "000",
        "0" :    "000",
        "M" :    "001",
        "D" :    "010",
        "MD" :   "011",
        "A" :    "100",
        "AM" :   "101",
        "AD" :   "110",
        "AMD" :  "111",
    }

    _comp_bin_code_table = {
        "" : "",
        "0" :   "0" + "101010",
        "1" :   "0" + "111111",
        "-1" :  "0" + "111010",
 
        "D" :   "0" + "001100",
        "A" :   "0" + "110000",
        "M" :   "1" + "110000",
 
        "!D" :  "0" + "001101",
        "!A" :  "0" + "110001",
        "!M" :  "1" + "110001",
 
        "-D" :  "0" + "001111",
        "-A" :  "0" + "110001",
        "-M" :  "1" + "110001",

        "D+1" : "0" + "011111",
        "A+1" : "0" + "110111",
        "M+1" : "1" + "110111",

        "D-1" : "0" + "001110",
        "A-1" : "0" + "110010",
        "M-1" : "1" + "110010",

        "D+A" : "0" + "000010",
        "D+M" : "1" + "000010",

        "D-A" : "0" + "010011",
        "D-M" : "1" + "010011",

        "A-D" : "0" + "000111",
        "M-D" : "1" + "000111",

        "D&A" : "0" + "000000",
        "D&M" : "1" + "000000",

        "D|A" : "0" + "010101",
        "D|M" : "1" + "010101",
    }

    _jump_bin_code_table = {
        "" : "000",
        "null" : "000",
        "0" :    "000",
        "JGT" :  "001",
        "JEQ" :  "010",
        "JGE" :  "011",
        "JLT" :  "100",
        "JNE" :  "101",
        "JLE" :  "110",
        "JMP" :  "111",
    }

    @classmethod
    def dest(cls, ins) -> str:
        return cls._dest_bin_code_table[ins]

    @classmethod
    def comp(cls, ins) -> str:
        return cls._comp_bin_code_table[ins]

    @classmethod
    def jump(cls, ins) -> str:
        return cls._jump_bin_code_table[ins]

    @classmethod
    def a_instrunction(cls, address) -> str:
        return "0" + "{0:015b}".format(address)