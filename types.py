from basic import *

class DotsParameter(Node):
    CODE = "210000"
    LABEL = "DotsParameter"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], DotsParameter.CODE)
        return DotsParameter(jsn['pos'])

class StructUnionName(Node):
    CODE = "60900"
    LABEL = "StructUnionName"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], StructUnionName.CODE)
        assert not jsn['children']
        return StructUnionName(jsn['pos'], jsn['label'])

    def __init__(self, pos, name):
        super().__init__(pos)
        self.__name = name

class TypeName(Node):
    CODE = "61000"
    LABEL = "TypeName"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], TypeName.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        return TypeName(jsn['pos'], children[0])

    def __init__(self, pos, name):
        super().__init__(pos)
        self.__name = name

class Pointer(Node):
    CODE = "60200"
    LABEL = "Pointer"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Pointer.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) <= 1
        typ = children[0] if children else None
        assert (typ is None) or isinstance(typ, FullType)
        return Pointer(jsn['pos'], typ)

    def __init__(self, pos, typ):
        super().__init__(pos)
        self.__typ = typ

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

class Void(Node):
    CODE = "70001"
    LABEL = "Void"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Void.CODE)
        return Void(jsn['pos'])

class CChar(Node):
    CODE = "80001"
    LABEL = "CChar"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], CChar.CODE)
        return CChar(jsn['pos'])

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
        assert len(children) <= 3
        
        qualifier = children.pop(0)
        if isinstance(children[0], TypeName):
            name = children.pop(0)
        else:
            name = None

        # Optional - may be Pointer or BaseType
        base_type = children.pop(0) if children else None

        assert isinstance(qualifier, TypeQualifier)
        assert name is None or isinstance(name, TypeName)
        assert base_type is None or isinstance(base_type, BaseType) or isinstance(base_type, Pointer)
        return FullType(jsn['pos'], qualifier, name, base_type)

    def __init__(self, pos, qualifier, name, base_type):
        super().__init__(pos)
        self.__qualifier = qualifier
        self.__name = name
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
