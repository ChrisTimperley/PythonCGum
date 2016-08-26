from basic import *

class Expression(Node):
    pass

class Identity(Expression):
    CODE = 240100
    LABEL = "Ident"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Identity.CODE
        of = jsn['children'][0]['label']
        return Identity(jsn['pos'], of)

    def __init__(self, pos, of):
        super().__init__(pos)
        self.of = of

class Constant(Expression):
    CODE = 240200
    LABEL = "Constant"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Constant.CODE
        return Constant(jsn['pos'], jsn['label'])

    def __init__(self, pos, value):
        super().__init__(pos)
        self.value = value

    def to_s(self):
        return str(self.value)

class FunctionCall(Expression):
    CODE = 240400
    LABEL = "FunCall"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == FunctionCall.CODE

        # Is it actually possible to call something other than through a direct
        # call to its name? I don't think so. Let's simplify. This does need to
        # be a node to be picked up by the Diff, though.
        function = Identity.from_json(jsn['children'][0])

        arguments = GenericList.from_json(jsn['children'][1])

# 242000 - ParenExpr
class Parentheses(Expression):
    pass

class Binary(Expression):
    CODE = 241100
    LABEL = "Binary"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Binary.CODE
        left = Node.from_json(jsn['children'][0]) 
        op = jsn['children'][1]['label']
        right = Node.from_json(jsn['children'][2])
        return Binary(jsn['pos'], left, op, right)

    def __init__(self, pos, left, op, right):
        super().__init__(pos)
        self.left = left
        self.op = op
        self.right = right

class Unary(Expression):
    pass
