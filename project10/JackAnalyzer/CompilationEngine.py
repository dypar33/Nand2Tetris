from JackTokenizer import JackTokenizer
from XMLWriter import XMLWriter
from SyntaxTable import *

class CompileException(Exception):
    def __init__(self, message='unknown error'):
        super().__init__(message)

class CompilationEngine:
    def __init__(self, input_file, file_path):
        self.input_file = input_file
        self.file_path = file_path
        self.tokenizer = JackTokenizer(self.file_path + "/" + input_file)
        self.token_writer = XMLWriter("{0}/{1}".format(file_path, input_file[:-5]+'T'), 'tokens')
        self.compile_result_writer = XMLWriter("{0}/{1}".format(file_path, input_file[:-5]), 'class')
        self.class_name = ""
        self.var_table = []
        self.class_var_table = []

    def _write_token(self, token_type, value):
        self.token_writer.write(token_type.value, " " + str(value) + " ")

    def _write_compile_result(self, key, value):
        self.compile_result_writer.write(key.value, " " + str(value) + " ")

    def _write_compile_result_for_sub_root(self, key):
        self.compile_result_writer.write_sub_root(key)

    def _write_compile_result_for_sub_root_end(self):
        self.compile_result_writer.end_sub_root()

    def _advance(self, comp_write=False, not_end=True) -> list:
        token_type = None

        while True:
            if not self.tokenizer.advance():
                if not_end:
                    raise CompileException('syntax error')
                return []
            
            token_type = self.tokenizer.get_token_type()
                        
            if token_type == TokenType.UNKNOWN:
                continue

            break
                    
        value = getattr(self.tokenizer, "get_" + token_type.name.lower())()

        self._write_token(token_type, value)

        if comp_write:
            self._write_compile_result(token_type, value)

        return [token_type, value]
    
    def _compile_keyword(self):
        result = self._advance(True)
        assert(result[0] == TokenType.KEYWORD)
        
        return result

    # handling access modifier
    def _compile_access_modifier(self):
        result = self._advance(True) 
        assert(result[0] == TokenType.KEYWORD)
    # handling type
    def _compile_type(self):
        result = self._advance(True)
        if result[1] == self.class_name:
            print(self.class_name)
            return
        
        assert(result[0] == TokenType.KEYWORD)
        
        return result

    def _compile_identifier(self):
        result = self._advance(True)
        assert(result[0] == TokenType.IDENTIFIER)

        return result

    def _compile_symbol(self, expect=""):
        result = self._advance(True)
        assert(result[0] == TokenType.SYMBOL)

        if expect:
            assert(result[1] == expect)

        return result

    def compile_class(self):
        self._compile_keyword()
        result = self._advance(False) # class name
        self.class_name = result[1]
        self._write_compile_result(*result)
        self._compile_symbol() # symbol

        result = self._advance(False)

        if result[1] not in VAR_ACCESS_MODIFIER_TABLE:
            self._write_compile_result_for_sub_root("classVarDec")
            self._write_compile_result_for_sub_root_end()

        while result[1] in VAR_ACCESS_MODIFIER_TABLE:
            self._write_compile_result_for_sub_root("classVarDec")

            self._write_compile_result(*result)
            self.compile_class_var_dec()

            self._write_compile_result_for_sub_root_end()
            
            result = self._advance(False)

        if result[1] not in FUNC_ACCESS_MODIFIER_TABLE:
            self._write_compile_result_for_sub_root("subroutineDec")
            self._write_compile_result_for_sub_root_end()

        while result[1] in FUNC_ACCESS_MODIFIER_TABLE:
            self._write_compile_result_for_sub_root("subroutineDec")

            self._write_compile_result(*result)
            self.compile_subroutine()

            self._write_compile_result_for_sub_root_end()

            result = self._advance(False)

        self._write_compile_result(*result) # '}'
        self.token_writer.write_end()
        self.compile_result_writer.write_end()

    def compile_class_var_dec(self):
        self._compile_type()
        result = self._compile_identifier() # var name
        self.class_var_table.append(result[1])
        
        while True:
            result = self._advance(False)

            if result[1] != ',':
                self._write_compile_result(*result) # ;
                break
            
            self._write_compile_result(*result)
            _, name = self._compile_identifier()
            self.class_var_table.append(name)


    def compile_subroutine(self):
        self.var_table.append([])

        # head
        self._compile_type() # return type
        self._compile_identifier() # function name

        self._compile_symbol() # (
        
        result = self._advance(False)
        if result[1] not in TYPE_TABLE:
            self._write_compile_result_for_sub_root("parameterList")
            self._write_compile_result_for_sub_root_end()

        while result[1] in TYPE_TABLE:
            self._write_compile_result_for_sub_root("parameterList")

            self._write_compile_result(*result)
            result = self.compile_parameter_list()

            self._write_compile_result_for_sub_root_end()

        self._write_compile_result(*result) # )

        # body
        self._write_compile_result_for_sub_root("subroutineBody")
        self._compile_symbol() # {
        
        result = self._advance(False)
        while result[1] == 'var':
            self._write_compile_result_for_sub_root("varDec")

            self._write_compile_result(*result)
            self.compile_var_dec()
            self._write_compile_result_for_sub_root_end()
                
            result = self._advance(False)
            
            self._write_compile_result_for_sub_root_end()

        result = self.compile_statements(result)
        self._write_compile_result(*result)

        self._write_compile_result_for_sub_root_end()

        self.var_table.pop()

    def compile_parameter_list(self) -> list:
        _, name = self._compile_identifier() # var name
        self.var_table[-1].append(name)

        while True:
            result = self._advance(False)

            if result[1] != ',':
                return result

            self._write_compile_result(*result)
            self._compile_type()
            _, var_name = self._compile_identifier()
            self.var_table[-1].append(var_name)

    def compile_var_dec(self):
        self._compile_type()
        _, name = self._compile_identifier() # var name
        self.var_table[-1].append(name)
        
        while True:
            result = self._advance(False)

            if result[1] != ',':
                self._write_compile_result(*result) # ;
                break
            
            self._write_compile_result(*result)
            _, name = self._compile_identifier()
            self.var_table[-1].append(name)

    def compile_statements(self, r_result=[]) -> list:
        self._write_compile_result_for_sub_root("statements")

        if r_result:
            result = r_result
        else:
            result = self._advance(False)

        while True:
            if result[1] not in STATEMENT_TABLE:
                self._write_compile_result_for_sub_root_end()
                return result
            
            result = getattr(self, 'compile_' + result[1])(result)
            
        
    def _compile_subroutine_call(self, result=[]):
        # function name or class/var name
        if result:
            self._write_compile_result(*result)
        else:
            self._compile_identifier()          

        result = self._advance(False)
        self._write_compile_result(*result) # . or (
        if result[1] == '.':
            self._compile_identifier()          # function or var name
            self._compile_symbol()              # (
            
        result = self.compile_expression_list()
        self._write_compile_result(*result) # )

    def compile_do(self, result) -> list:
        self._write_compile_result_for_sub_root("doStatement")

        self._write_compile_result(*result) # do keyword

        # result = self._advance(False)
        #if result[1] == self.class_name or result[1] in self.var_table:
            #self._write_compile_result(*result) # class or var name
            #self._compile_symbol()              # (

        self._compile_subroutine_call()
        self._compile_symbol()              # ;

        self._write_compile_result_for_sub_root_end()
        
        result = self._advance(False)
        return result

    def compile_let(self, result) -> list:
        self._write_compile_result_for_sub_root("letStatement")

        self._write_compile_result(*result) # let keyword
        
        self._compile_identifier() # var name

        result = self._advance(False)
        if result[1] == '[':
            self._write_compile_result(*result) # [
            result = self.compile_expression()
            self._write_compile_result(*result) # ]

            result = self._advance(False)
        
        assert(result[1] == '=')
        self._write_compile_result(*result)

        result = self.compile_expression()

        self._write_compile_result(*result) # ;
        
        self._write_compile_result_for_sub_root_end()
        
        result = self._advance(False)
        return result

    def compile_while(self, result) -> list:
        self._write_compile_result_for_sub_root("whileStatement")

        self._write_compile_result(*result) # while keyword
        self._compile_symbol() # (

        result = self.compile_expression()
        self._write_compile_result(*result) # )
        
        
        self._compile_symbol() # {
        result = self.compile_statements()
        self._write_compile_result(*result) # }
        
        self._write_compile_result_for_sub_root_end()

        result = self._advance(False)
        return result

    def compile_return(self, result) -> list:
        self._write_compile_result_for_sub_root("returnStatement")

        self._write_compile_result(*result) # return keyword

        result = self._advance(False)

        if result[1] != ';':
            result = self.compile_expression(result)
            self._write_compile_result(*result) # ;
        else:
            self._write_compile_result(*result)
        
        self._write_compile_result_for_sub_root_end()
        
        result = self._advance(False)
        return result

    def compile_if(self, result) -> list:
        self._write_compile_result_for_sub_root("ifStatement")

        self._write_compile_result(*result) # if keyword
        
        self._compile_symbol() # (
        
        result = self.compile_expression()
        self._write_compile_result(*result) # )
        
        
        self._compile_symbol() # {
        result = self.compile_statements()
        self._write_compile_result(*result) # }

        result = self._advance(False)
        if result[1] == 'else':
            self._write_compile_result(*result) # else keyword
            self._compile_symbol() # {
            result = self.compile_statements()
            self._write_compile_result(*result) # }

            result = self._advance(False)

        self._write_compile_result_for_sub_root_end()
        return result
    
    def compile_expression(self, r_result=[]) -> list:
        self._write_compile_result_for_sub_root("expression")

        while True:
            if r_result:
                self.compile_term(r_result)
                r_result=[]
            else:
                self.compile_term()
            result = self._advance(False)

            if result[1] in OPERATION_TABLE:
                self._write_compile_result(*result)
                continue
                
            self._write_compile_result_for_sub_root_end()
            return result

    def _search_var(self, target):
        for var in self.var_table:
            if isinstance(var, list):
                for var_2 in var:
                    if var_2 == target:
                        return True
                    
                continue
            
            if var == target:
                return True

    def compile_term(self, result=[]):
        self._write_compile_result_for_sub_root("term")

        if not result:
            result = self._advance(False)
        print(result)

        if result[0] == TokenType.INT_CONST or result[0] == TokenType.STRING_CONST or result[1] in KEYWORD_CONSTANT_TABLE or self._search_var(result[1]) or result[1] in self.class_var_table:
            self._write_compile_result(*result)
            # TODO array handling
        # sub routine call
        elif result[0] == TokenType.IDENTIFIER:
            self._compile_subroutine_call(result)
        elif result[1] == '(':
            self._write_compile_result(*result) # (
            result = self.compile_expression()
            self._write_compile_result(*result) # )
        elif result[1] in UNARY_OPERATION_TABLE:
            self._write_compile_result(*result)
            self.compile_term()
        else:
            self.compile_result_writer.write_end()
            raise CompileException('term error / {0} "{1}"'.format(*result)) 

        self._write_compile_result_for_sub_root_end()

    def compile_expression_list(self) -> list:
        self._write_compile_result_for_sub_root("expressionList")
        
        while True:
            result = self._advance()
            if result[1] == ')':
                self._write_compile_result_for_sub_root_end()
                return result
            result = self.compile_expression(result)

            if result[1] != ',':
                self._write_compile_result_for_sub_root_end()
                return result
            
            self._write_compile_result(*result)