from basic import *

class Expression(Node):
    pass

class Identity(Expression):
    CODE = 240100
    LABEL = "Ident"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Identity.CODE
        of = GenericString.from_json(jsn['children'][0])
        return Identity(jsn['pos'], of)

    def __init__(self, pos, of):
        super().__init__(pos)
        self.__of = of

    def of(self):
        return self.__of.read()

class Constant(Expression):
    CODE = 240200
    LABEL = "Constant"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Constant.CODE
        return Constant(jsn['pos'], jsn['label'])

    def __init__(self, pos, value):
        super().__init__(pos)
        self.__value = value

    def value(self):
        return self.__value

    def to_s(self):
        return str(self.__value)

class FunctionCall(Expression):
    CODE = 240400
    LABEL = "FunCall"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == FunctionCall.CODE
        function = Identity.from_json(jsn['children'][0])
        arguments = GenericList.from_json(jsn['children'][1])
        return FunctionCall(jsn['pos'], function, arguments)

    def __init__(self, pos, function, arguments):
        super().__init__(pos)
        self.__function = function
        self.__arguments = arguments

    # Returns the AST nodes containing the arguments to this function
    def arguments(self):
        pass

class Parentheses(Expression):
    CODE = 242000
    LABEL = "ParenExpr"

class Unary(Expression):
    CODE = 241000
    LABEL = "Unary"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Unary.CODE
        operand = Node.from_json(jsn['children'][0])
        operator = GenericString.from_json(jsn['children'][1])
        return Unary(jsn['pos'], operand, operator)

    def __init__(self, pos, operand, operator):
        super().__init__(pos)
        self.__operand = operand
        self.__operator = operator

class Binary(Expression):
    CODE = 241100
    LABEL = "Binary"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Binary.CODE
        left = Node.from_json(jsn['children'][0]) 
        op = GenericString.from_json(jsn['children'][1])
        right = Node.from_json(jsn['children'][2])
        return Binary(jsn['pos'], left, op, right)

    def __init__(self, pos, left, op, right):
        super().__init__(pos)
        self.__left = left
        self.__op = op
        self.__right = right

    def op(self):
        return self.__op.label()
