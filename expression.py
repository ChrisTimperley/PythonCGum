from basic import *

# Base class used by all AST nodes deemed to represent a C expression
class Expression(Node):
    pass

class Sequence(Expression):
    CODE = "240600"
    LABEL = "Sequence"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Sequence.CODE)
        return Sequence(jsn['pos'],\
                        [Node.from_json(c) for c in jsn['children']])

    def __init__(self, pos, exprs):
        super().__init__(pos)
        self.__exprs = exprs

class ArrayAccess(Expression):
    CODE = "241200"
    LABEL = "ArrayAccess"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], ArrayAccess.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 2
        return ArrayAccess(jsn['pos'], children[0], children[1])

    def __init__(self, pos, arr, index):
        super().__init__(pos)
        self.__arr = arr
        self.__index = index

# Not entirely sure what this is meant to be?
# It has no children, so either it ignores the type whose size it measures, or
# it does something entirely different.
class SizeOfType(Expression):
    CODE = "241600"
    LABEL = "SizeOfType"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], SizeOfType.CODE)
        assert not jsn['children']
        return SizeOfType(jsn['pos'])

class Assignment(Expression):
    CODE = "240700"
    LABEL = "Assignment"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Assignment.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 3
        assert isinstance(children[1], GenericString)
        return Assignment(jsn['pos'], children[0], children[2])

    def __init__(self, pos, lhs, rhs):
        super().__init__(pos)
        self.__lhs = lhs
        self.__rhs = rhs

# This seems to just represent Postfix expressions? This has nothing to do with
# Infix expression?
class Infix(Expression):
    CODE = "240900"
    LABEL = "Infix"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Infix.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 2
        return Infix(jsn['pos'], children[0], children[1])

    def __init__(self, pos, operand, operator):
        super().__init__(pos)
        self.__operand = operand
        self.__operator = operator

class Postfix(Expression):
    CODE = "240800"
    LABEL = "Postfix"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Postfix.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 2
        assert isinstance(children[1], GenericString)
        return Postfix(jsn['pos'], children[0], children[1])

    def __init__(self, pos, operand, operator):
        super().__init__(pos)
        self.__operand = operand
        self.__operator = operator

class RecordPtAccess(Expression):
    CODE = "241400"
    LABEL = "RecordPtAccess"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], RecordPtAccess.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert isinstance(children[1], GenericString) 
        return RecordPtAccess(jsn['pos'],\
                              children[0],
                              children[1])

    def __init__(self, pos, expr, member):
        super().__init__(pos)
        self.__expr = expr
        self.__member = member

class Identity(Expression):
    CODE = "240100"
    LABEL = "Ident"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Identity.CODE)
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
    CODE = "240200"
    LABEL = "Constant"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Constant.CODE)
        return Constant(jsn['pos'], jsn['label'])

    def __init__(self, pos, value):
        super().__init__(pos)
        self.__value = value

    def value(self):
        return self.__value

    def to_s(self):
        return str(self.__value)

class Cast(Expression):
    CODE = "241700"
    LABEL = "Cast"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Cast.CODE)
        expr = Node.from_json(jsn['children'][0])
        return Cast(jsn['pos'], expr)

    def __init__(self, pos, expr):
        super().__init__(pos)
        self.__expr = expr

    def to_s(self):
        return "(UNKNOWN_TYPE) %s" % self.__expr.to_s()

# What is the difference between Init and Assignment?
class InitExpr(Expression):
    CODE = "360100"
    LABEL = "InitExpr"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], InitExpr.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        return InitExpr(jsn['pos'], children)

    def __init__(self, pos, expr):
        super().__init__(pos)
        self.__expr = expr

class Ternary(Expression):
    CODE = "240500"
    LABEL = "CondExpr"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Ternary.CODE)
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
    CODE = "240400"
    LABEL = "FunCall"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], FunctionCall.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 2
        assert isinstance(children[1], GenericList)
        return FunctionCall(jsn['pos'], children[0], children[1])

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
    CODE = "242000"
    LABEL = "ParenExpr"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Parentheses.CODE)
        expr = Node.from_json(jsn['children'][0])
        return Parentheses(jsn['pos'], expr)

    def __init__(self, pos, expr):
        super().__init__(pos)
        self.__expr = expr

    def expr(self):
        return self.__expr

    def to_s(self):
        return "(%s)" % self.__expr.to_s()

# I really have no idea what the point of this node is? Seems to contain nodes
# whose presence is otherwise optional. In the case those nodes are missing, a
# None can be found instead.
# From observation, it only ever seems to contain one item, followed by a ;
class Some(Node):
    CODE = "290100"
    LABEL = "Some"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Some.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) <= 2
        expr = children[0]
        if len(children) == 2:
            semi_colon = children[1]
            assert isinstance(semi_colon, GenericString)
            assert semi_colon.to_s() == ";"
        else:
            semi_colon = None
        return Some(jsn['pos'], expr, semi_colon)

    def __init__(self, pos, expr, semicolon):
        super().__init__(pos)
        self.__expr = expr
        self.__semicolon = semicolon

class Unary(Expression):
    CODE = "241000"
    LABEL = "Unary"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Unary.CODE)
        operand = Node.from_json(jsn['children'][0])
        operator = GenericString.from_json(jsn['children'][1])
        return Unary(jsn['pos'], operand, operator)

    def __init__(self, pos, operand, operator):
        super().__init__(pos)
        self.__operand = operand
        self.__operator = operator

class Binary(Expression):
    CODE = "241100"
    LABEL = "Binary"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Binary.CODE)
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

class ReturnExpr(Expression):
    CODE = "280200"
    LABEL = "ReturnExpr"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], ReturnExpr.CODE)
        return ReturnExpr(jsn['pos'],\
                          Node.from_json(jsn['children'][0]))

    def __init__(self, pos, expr):
        super().__init__(pos)
        self.__expr = expr

    def to_s(self):
        return "return %s" % self.__expr.to_s()
