class DuplicateDeclaration(Exception):
    def __init__(self, line_number=0):
        super().__init__('{}줄 중복 선언 감지됨', line_number)

class SyntaxError(Exception):
    def __init__(self, line_number=0):
        super().__init__('{}줄 문법 오류 감지됨', line_number)