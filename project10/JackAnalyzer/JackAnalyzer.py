from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from XMLWriter import XMLWriter
from SyntaxTable import TokenType

import sys, os

class JackAnalyzer:
    def __init__(self, file_list, file_path):
        self.file_list = file_list
        self.file_path = file_path

    """def tokenize(self):
        for file in self.file_list:
            #with open("{0}/{1}{2}".format(self.file_path, file[:-4], "xml"), 'w') as f:
            xml_writer = XMLWriter("{0}/{1}".format(self.file_path, file[:-4]), 'tokens')
            tokenizer = JackTokenizer(self.file_path + "/" + file)
                
            while tokenizer.advance():
                token_type = tokenizer.get_token_type()
                    
                value = getattr(tokenizer, "get_" + token_type.name.lower())()

                if token_type == TokenType.UNKNOWN:
                    continue
                
                xml_writer.write_to_root(token_type.value, " " + str(value) + " ")

            xml_writer.write_end()"""

    def compile(self):
        for file in self.file_list:
            compilation_engine = CompilationEngine(file, self.file_path)
            compilation_engine.compile_class()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: JackAnalyzer.py [target file or directory]")

    jack_files = []

    if os.path.isdir(sys.argv[1]):
        path = sys.argv[1]

        for file_name in os.listdir(sys.argv[1]):
            if file_name.endswith(".jack"):
                jack_files.append(file_name)
    else:
        path = os.path.split(sys.argv[1])[0]
        jack_files.append(sys.argv[1])

    jack_analyzer = JackAnalyzer(jack_files, path)
    jack_analyzer.compile()