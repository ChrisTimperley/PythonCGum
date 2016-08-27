from basic import *
import statement
import preprocessor

class FunctionParameter(Node):
    CODE = "220100"
    LABEL = "ParameterType"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], FunctionParameter.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) <= 1
        name = children[0] if children else None
        return FunctionParameter(jsn['pos'],\
                                 (children[0] if children else None))

    def __init__(self, pos, name):
        super().__init__(pos)
        self.__name = name

    def incomplete(self):
        return self.__name is None

    def name(self):
        return self.__name.read()

    def to_s(self):
        return self.__name.to_s()

class FunctionParameters(Node):
    CODE = "200000"
    LABEL = "ParamList"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], FunctionParameters.CODE)
        params = [FunctionParameter.from_json(c) for c in jsn['children']]
        return FunctionParameters(jsn['pos'], params)

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
        if isinstance(children[0], statement.Storage):
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
        assert isinstance(block, statement.Block)

        return FunctionDefinition(jsn['pos'], name, params, block, storage)

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
