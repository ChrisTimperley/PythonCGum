from basic import *

# Represents a C preprocessor statement
class PreprocessorStatement(Node):
    CODE = "450300"
    LABEL = "CppTop"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], PreprocessorStatement.CODE)
        return PreprocessorStatement(jsn['pos'],\
                                     OtherDirective.from_json(jsn['children'][0]))

    def __init__(self, pos, statement):
        super().__init__(pos)
        self.__statement = statement

    def to_s(self):
        return self.__statement.to_s()

class OtherDirective(Node):
    CODE = "400400"
    LABEL = "OtherDirective"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], OtherDirective.CODE)
        return OtherDirective(jsn['pos'],\
                              GenericString.from_json(jsn['children'][0]))
    
    def __init__(self, pos, directive):
        super().__init__(pos)
        self.__directive = directive

    def to_s(self):
        return self.__directive.to_s()
