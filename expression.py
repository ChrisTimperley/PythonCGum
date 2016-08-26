from basic import *

# Base class used by all AST nodes deemed to represent a C expression
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

    def to_s(self):
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

class Cast(Expression):
    CODE = 241700
    LABEL = "Cast"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Cast.CODE
        expr = Node.from_json(jsn['children'][0])
        return Cast(jsn['pos'], expr)

    def __init__(self, pos, expr):
        super().__init__(pos)
        self.__expr = expr

    def to_s(self):
        return "(UNKNOWN_TYPE) %s" % self.__expr.to_s()

# Does not specify the variable that is being assigned to. A little bit
# annoying. Is InitExpr not assignment?
class Assignment(Expression):
    CODE = 

class Ternary(Expression):
    CODE = 240500
    LABEL = "CondExpr"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Ternary.CODE
        return Ternary(jsn['pos'],\
                       Node.from_json(jsn['children'][0]),\
                       Node.from_json(jsn['children'][1]),\
                       Node.from_json(jsn['children'][2]))

    def __init__(self, pos, cond, then, els):
        super().__init__(pos)
        self.__cond = cond
        self.__then = then
        self.__els = els

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

    # Returns the name of the function the call was made to
    def function(self):
        return self.__function.to_s()

    # Returns the AST nodes containing the arguments to this function
    def arguments(self):
        pass

class Parentheses(Expression):
    CODE = 242000
    LABEL = "ParenExpr"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Parentheses.CODE
        expr = Node.from_json(jsn['children'][0])
        return Parentheses(jsn['pos'], expr)

    def __init__(self, pos, expr):
        super().__init__(pos)
        self.__expr = expr

    def expr(self):
        return self.__expr

    def to_s(self):
        return "(%s)" % self.__expr.to_s()

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

class Return(Expression):
    CODE = 280200
    LABEL = "ReturnExpr"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Return.CODE
        return Return(jsn['pos'],\
                      Node.from_json(jsn['children'][0]))

    def __init__(self, pos, expr):
        super().__init__(pos)
        self.__expr = expr

    def to_s(self):
        return "return %s" % self.__expr.to_s()
