from basic import *
import statement
import preprocessor

class FunctionParameter(Node):
    CODE = "220100"
    LABEL = "ParameterType"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], FunctionParameter.CODE)
        return FunctionParameter(jsn['pos'],\
                                 Node.from_json(jsn['children'][0]))

    def __init__(self, pos, name):
        super().__init__(pos)
        self.__name = name

    def name(self):
        return self.__name.read()

    def to_s(self):
        return self.__name.to_s()

class FunctionParameterList(Node):
    CODE = "200000"
    LABEL = "ParamList"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], FunctionParameterList.CODE)
        params = [FunctionParameter.from_json(c) for c in jsn['children']]
        return FunctionParameterList(jsn['pos'], params)

    def __init__(self, pos, params):
        super().__init__(pos)
        self.__params = params

    def parameters(self):
        return [p.name() for p in self.__params]

class FunctionDefinition(Node):
    CODE = "380000"
    LABEL = "Definition"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], FunctionDefinition.CODE)
        children = [Node.from_json(c) for c in jsn['children']]

        # Find any optional storage information for this function
        if isinstance(children[0], Storage):
            storage = children.pop(0)
        else:
            storage = None

        # Get the required information for the function
        params = children[0]
        name = children[1]
        block = children[2]

        # Do some sanity checking
        assert isinstance(params, FunctionParameters)
        assert isinstance(name, GenericString)
        assert isinstance(block, Block)

        return FunctionDefinition(jsn['pos'], name, params, block)

    def __init__(self, pos, name, parameters, block, storage):
        super().__init__(pos)
        self.__name = name
        self.__parameters = parameters
        self.__block = block
        self.__storage = storage

# Represents the root AST node for a program
# For now we just get all the "components" of a program and worry about what
# kind of components they might be later.
class Program(Node):
    CODE = "460000"
    LABEL = "Program"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Program.CODE)
        return Program(jsn['pos'],\
                       [Node.from_json(c) for c in jsn['children']])

    def __init__(self, pos, components):
        super().__init__(pos)
        self.__components = components
