from basic import *
import expression

class Statement(Node):
    pass

# What is this?
class Si(Node):
    CODE = "80100"
    LABEL = "Si"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Si.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 1
        return Si(jsn['pos'], children[0])

    def __init__(self, pos, typ):
        super().__init__(pos)
        self.__typ = typ

# And this?
class CInt(Node):
    CODE = "100003"
    LABEL = "CInt"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], CInt.CODE)
        return CInt(jsn['pos'])

class IntType(Node):
    CODE = "70100"
    LABEL = "IntType"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], IntType.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 1
        return IntType(jsn['pos'], children[0])

    def __init__(self, pos, typ):
        super().__init__(pos)
        self.__typ = typ

# TODO: Exactly what is this implementing?
class BaseType(Node):
    CODE = "60100"
    LABEL = "BaseType"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], BaseType.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 1
        return BaseType(jsn['pos'], children[0])

    def __init__(self, pos, base):
        super().__init__(pos)
        self.__base = base

class TypeQualifier(Node):
    CODE = "50000"
    LABEL = "TypeQualifier"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], TypeQualifier.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 1 and isinstance(children[0], GenericString)
        return TypeQualifier(jsn['pos'], children[0])

    def __init__(self, pos, qualifier):
        super().__init__(pos)
        self.__qualifier = qualifier

# Provides a full type definition
class FullType(Node):
    CODE = "40000"
    LABEL = "FullType"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], FullType.CODE)
        children = [Node.from_json(c) for c in jsn['children']]

        qualifier = children[0]
        base_type = children[1]

        assert isinstance(qualifier, TypeQualifier)
        assert isinstance(base_type, BaseType)

        return FullType(jsn['pos'], qualifier, base_type)

    def __init__(self, pos, qualifier, base_type):
        super().__init__(pos)
        self.__qualifier = qualifier
        self.__base_type = base_type

class Storage(Node):
    CODE = "340000"
    LABEL = "Storage"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Storage.CODE)
        return Storage(jsn['pos'],\
                       GenericString.from_json(jsn['children'][0]))

    def __init__(self, pos, label):
        super().__init__(pos)
        self.__label = label

class DeclarationList(Node):
    CODE = "350100"
    LABEL = "DeclList"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], DeclarationList.CODE)
        return DeclarationList(jsn['pos'],\
                               [Node.from_json(c) for c in jsn['children']])

    def __init__(self, pos, declarations):
        super().__init__(pos)
        self.__declarations = declarations

# A declaration isn't quite a statement, but this is the best place for it,
# for now.
class Declaration(Node):
    CODE = "450100"
    LABEL = "Declaration"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Declaration.CODE)
        return Declaration(jsn['pos'],\
                           DeclarationList.from_json(jsn['children'][0]))

    def __init__(self, pos, declared):
        super().__init__(pos)
        self.__declared = declared

# Generic definition class
class Definition(Node):
    CODE = "450200"
    LABEL = "Definition"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Definition.CODE)
        return Definition(jsn['pos'],\
                          Node.from_json(jsn['children'][0]))

    def __init__(self, pos, defined):
        super().__init__(pos)
        self.__defined = defined

    def defined(self):
        return self.__defined

    def to_s(self):
        return self__defined.to_s()


class ExprStatement(Node):
    pass

# Never seems to return the result of an expression?
class Return(Statement):
    CODE = "280003"
    LABEL = "Return"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Return.CODE)
        return Return(jsn['pos'])

    def to_s(self):
        return "return;"

class IfElse(Statement):
    CODE = "300100"
    LABEL = "If"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], IfElse.CODE)
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
    CODE = "330000"
    LABEL = "Compound"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Block.CODE)
        return Block(jsn['pos'],\
                     [Node.from_json(c) for c in jsn['children']])

    def __init__(self, pos, contents):
        super().__init__(pos)
        self.__contents = contents
