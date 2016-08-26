class Expression(Node):
    pass

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


