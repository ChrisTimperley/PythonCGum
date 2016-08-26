from basic import *
import expression

class Statement(Node):
    pass

class ExprStatement(Node):
    pass

# Never seems to return the result of an expression?
class Return(Statement):
    CODE = 280003
    LABEL = "Return"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Return.CODE
        return Return(jsn['pos'])

class IfElse(Statement):
    CODE = 300100
    LABEL = "If"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == IfElse.CODE 

        condition = Node.from_json(jsn['children'][1])
        then = Node.from_json(jsn['children'][2])

        # Build the "else" branch, if there is one.
        if len(jsn['children']) == 4:
            els = Node.from_json(jsn['children'][3])
        else:
            els = None

        return IfElse(jsn['pos'], condition, then, els)

    def __init__(self, pos, condition, then, els):
        super().__init__(pos)
        self.__condition = condition
        self.__then = then
        self.__els = els

class Block(Node):
    CODE = 330000
    LABEL = "Compound"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Block.CODE
        return Block(jsn['pos'],\
                     [Node.from_json(c) for c in jsn['children']])

    def __init__(self, pos, contents):
        super().__init__(pos)
        self.__contents = contents

class FunctionParameter(Node):
    CODE = 220100
    LABEL = "ParameterType"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == FunctionParameter.CODE
        return FunctionParameter(jsn['pos'], jsn['children'][0]['label'])

    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name

class FunctionDefinition(basic.Node):
    CODE = 380000
    LABEL = "Definition"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == FunctionDefinition.CODE

        # Fetch the name
        name = jsn['children'][1]['label']
        
        # Build the parameters
        parameters = jsn['children'][0]
        assert parameters['typeLabel'] == 'ParamList',\
            "expected first child of Definition to be ParamList"
        parameters = parameters['children']
        parameters = [FunctionParameter.from_json(c) for c in parameters]

        # Build the statements
        statements = Block.from_json(jsn['children'][2])
        statements = statements.statements

        return FunctionDefinition(jsn['pos'], name, parameters, statements)

    def __init__(self, pos, name, parameters, statements):
        super().__init__(pos)
        self.name = name
        self.parameters = parameters
        self.statements = statements


