from SyntaxTable import *
from collections import deque

class JackTokenizer:
    current_token_list = deque()
    current_token = ""
    current_token_value = ""
    is_in_multiline_comment = False

    def __init__(self, input_file):
        self.target_file_fd = open(input_file, 'r')

    def _next_line(self) -> bool:
        line = self.target_file_fd.readline()
        
        if line == '':
            return False
        
        self.current_line = line.strip()

        return True
    
    def _tokenizing(self):
        line = self.current_line

        # remove one-line comment
        line = ONELINE_COMMENT_REGEX.sub('', line)

        # check is in mutipleline_comment
        if self.is_in_multiline_comment:
            if is_mutiline_comment_end:= MUTILINE_COMMENT_CLOSE_REGEX.search(line):
                self.is_in_multiline_comment = False

                line = line[is_mutiline_comment_end.end():]
            else:
                return []

        # if multi line comment exists
        if is_mutiline_comment_start := MUTILINE_COMMENT_OPEN_REGEX.search(line):
            if is_mutiline_comment_end:= MUTILINE_COMMENT_CLOSE_REGEX.search(line):
                tmp_line = line[:is_mutiline_comment_start.start()]
                line = tmp_line + line[is_mutiline_comment_end.end():]
            else:
                line = line[:is_mutiline_comment_start.start()]
                self.is_in_multiline_comment = True

        self.current_token_list = deque(TOKEN_EXTRACT_REGEX.findall(line))

    def advance(self) -> bool:
        if not self.current_token_list:
            if not self._next_line():
                return False
            else:
                self._tokenizing()

        if self.current_token_list:
            self.current_token = self.current_token_list.popleft()
        else:
            self.current_token = ""

        return True

    def get_token_type(self) -> TokenType:
        token = self.current_token

        if (result := KEYWORD_REGEX.match(token)):
            self.current_token_value = result.group()
            return TokenType.KEYWORD
        elif (result := SYMBOL_REGEX.match(token)):
            self.current_token_value = result.group()
            return TokenType.SYMBOL
        elif (result := INTEGER_CONSTANT_REGEX.match(token)):
            self.current_token_value = result.group()
            return TokenType.INT_CONST
        elif (result := STRING_CONSTANT_REGEX.match(token)):
            self.current_token_value = result.group()
            return TokenType.STRING_CONST
        elif (result := IDENTIFIER_REGEX.match(token)):
            self.current_token_value = result.group()
            return TokenType.IDENTIFIER
        else:
            self.current_token_value = ""
            return TokenType.UNKNOWN

    def get_keyword(self) -> str: # KEYWORD
        return self.current_token_value

    def get_symbol(self) -> str:
        return self.current_token_value

    def get_identifier(self) -> str:
        return self.current_token_value
    
    def get_int_const(self) -> int:
        return int(self.current_token_value)

    def get_string_const(self) -> str:
        return self.current_token_value[1:-1]

    def get_unknown(self):
        print("Unknown token")