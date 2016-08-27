from basic import *
import statement
import preprocessor
import types

class FunctionParameter(Node):
    CODE = "220100"
    LABEL = "ParameterType"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) <= 2

        # Find the optional type and name of this parameter
        tmp = children.copy()
        self.__typ = \
            tmp.pop(0) if (tmp and isinstance(tmp[0], types.FullType)) else None
        self.__name = tmp.pop(0) if tmp else None

        assert self.__typ is None or isinstance(typ, types.FullType)
        assert self.__name is None or isinstance(self.__name, GenericString)
        super().__init__(pos, length, label, children)

    def is_incomplete(self):
        return self.name() is None
    def typ(self):
        return self.__typ.to_s() if self.__typ else None
    def name(self):
        return self.__name.to_s() if self.__name else None

class FunctionParameters(Node):
    CODE = "200000"
    LABEL = "ParamList"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert all([isinstance(c, FunctionParameter) for c in children])
        super().__init__(pos, length, label, children)

    def parameters(self):
        return self.__children

class FunctionDefinition(Node):
    CODE = "380000"
    LABEL = "Definition"

    @staticmethod
    def from_json(jsn):
                return FunctionDefinition(jsn['pos'], name, params, block, storage, dots)

    def __init__(self, pos, length, label, children):
        assert len(children) >= 3 and len(children) <= 5

        tmp = children.copy()
        self.__storage = \
            tmp.pop(0) if isinstance(tmp[0], types.Storage) else None
        self.__parameters = tmp.pop(0)
        self.__dots = \
            tmp.pop(0) if isinstance(tmp[0], types.DotParameter) else None
        self.__name = tmp.pop(0)
        self.__block = tmp.pop(0)

        assert isinstance(self.__parameters, FunctionParameters)
        assert self.__dots is None or \
            isinstance(self.__dots, types.DotsParameter)
        assert self.__storage is None or \
            isinstance(self.__storage, types.Storage)
        assert isinstance(self.__name, GenericString)
        assert isinstance(self.__block, statement.Block)
        super().__init__(pos, length, label, children)

    def name(self):
        return self.__name
    def parameters(self):
        return self.__parameters
    def block(self):
        return self.__block
    def storage(self):
        return self.__storage
    def dots(self):
        return self.__dots

    def is_variadic(self):
        return not (self.dots() is None)

# Used to mark the end of the program!
class FinalDef(Token):
    CODE = "450800"
    LABEL = "FinalDef"

# Represents the root AST node for a program
# For now we just get all the "components" of a program and worry about what
# kind of components they might be later.
class Program(Node):
    CODE = "460000"
    LABEL = "Program"
