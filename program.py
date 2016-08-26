from basic import *
import statement

class FunctionParameter(Node):
    CODE = 220100
    LABEL = "ParameterType"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == FunctionParameter.CODE
        return FunctionParameter(jsn['pos'],\
                                 Node.from_json(jsn['children'][0]))

    def __init__(self, pos, name):
        super().__init__(pos)
        self.__name = name

    def name(self):
        return self.__name.read()

    def to_s(self):
        return self.__name.to_s()

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

# Represents the root AST node for a program
class Program(Node):
    CODE = 460000
    LABEL = "Program"

    @staticmethod
    def from_json(jsn):
        pass
