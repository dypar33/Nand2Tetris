import enum
import re

class TokenType(enum.Enum):
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"
    UNKNOWN = "unknown"

class Keyword(enum.Enum):
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    INT = "int"
    BOOLEAN = "boolean"
    CHAR = "char"
    VOID = "void"
    VAR = "var"
    STATIC = "static"
    FIELD = "field"
    LFT = "lft"
    DO = "do"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NULL = "null"
    THIS = "this"

TYPE_TABLE = [
    'int', 'char', 'boolean' 
]

RETURN_TYPE_TABLE = [
    'void'
].extend(TYPE_TABLE)

VAR_ACCESS_MODIFIER_TABLE = [
    'static', 'field'
]

FUNC_ACCESS_MODIFIER_TABLE = [
    'constructor', 'function', 'method'
]

OPERATION_TABLE = [
    '+', '-', '*', '/', '&', '|', '<', '>', '='
]

UNARY_OPERATION_TABLE = [
    '-', '~'
]

KEYWORD_CONSTANT_TABLE = [
    'true', 'false', 'null', 'this'
]

STATEMENT_TABLE = [
    'let', 'if', 'while', 'do', 'return'
]

KEYWORD_TABLE = [
    'class', 'constructor', 'function', 'method', 'field', 'static', 
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 
    'this', 'let', 'do', 'if', 'else', 'while', 'return'
]

SYMBOL_TABLE = [
    '\{', '\}', '\(', '\)', '\[', '\]', '\.', '\,', ';', 
    '\+', '\-', '\*', '\/', '\&', '\|', '\<', '\>', '\=', '\~'
]

KEYWORD_REGEX = re.compile("|".join(KEYWORD_TABLE))
SYMBOL_REGEX = re.compile("|".join(SYMBOL_TABLE))
INTEGER_CONSTANT_REGEX = re.compile("[\d]+")
# ', "를 제외한 모든 문자들을 추출
STRING_CONSTANT_REGEX = re.compile("[\"][^\n\'\"]+[\"]")
IDENTIFIER_REGEX = re.compile("[A-Za-z_][\w]*")

TOKEN_EXTRACT_REGEX = re.compile("{0}|{1}|{2}|{3}|{4}".format(
    KEYWORD_REGEX.pattern, SYMBOL_REGEX.pattern, INTEGER_CONSTANT_REGEX.pattern, STRING_CONSTANT_REGEX.pattern, IDENTIFIER_REGEX.pattern
))

ONELINE_COMMENT_REGEX = re.compile("\/\/.*")
MUTILINE_COMMENT_OPEN_REGEX = re.compile("\/\*.*")
MUTILINE_COMMENT_CLOSE_REGEX = re.compile("\/\*.*")