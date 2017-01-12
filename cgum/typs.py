from cgum.basic import *

class DotsParameter(Token):
    CODE = "210000"
    LABEL = "DotsParameter"

class StructUnion(Node):
    CODE = "60700"
    LABEL = "StructUnion"

class StructUnionName(Node):
    CODE = "60900"
    LABEL = "StructUnionName"

    def __init__(self, pos, length, label, children):
        assert isinstance(label, str)
        assert not children
        super().__init__(pos, length, label, children)

    def name(self):
        return self.label()

class TypeName(Node):
    CODE = "61000"
    LABEL = "TypeName"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)
    
    def name(self):
        return self.__children[0].to_s()

class Pointer(Node):
    CODE = "60200"
    LABEL = "Pointer"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) <= 1
        assert (not children) or isinstance(children[0], FullType)
        super().__init__(pos, length, label, children) 
    
    def typ(self):
        return children[0] if children else None

# What is this?
class Si(Node):
    CODE = "80100"
    LABEL = "Si"

    def __init__(self, pos, length, label, children):
        assert label is None
        #assert len(children) == 1
        super().__init__(pos, length, label, children)

    def typ(self):
        return self.__children[0]

class EnumName(Node):
    CODE = "60800"
    LABEL = "EnumName"

class UnSigned(Node):
    CODE = "90002"
    LABEL ="UnSigned"

class Void(Token):
    CODE = "70001"
    LABEL = "Void"

class CChar(Token):
    CODE = "80001"
    LABEL = "CChar"

class CInt(Token):
    CODE = "100003"
    LABEL = "CInt"

class CFloat(Token):
    CODE = "110001"
    LABEL = "CFloat"

class CDouble(Token):
    CODE = "110002"
    LABEL = "CDouble"

class CLong(Token):
    CODE = "100004"
    LABEL = "CLong"

class CLongLong(Token):
    CODE = "100005"
    LABEL = "CLongLong"

class SizeType(Token):
    CODE = "70002"
    LABEL = "SizeType"

class FloatType(Node):
    CODE = "70200"
    LABEL = "FloatType"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

# Not sure about this?
class IntType(Node):
    CODE = "70100"
    LABEL = "IntType"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

# TODO: Exactly what is this implementing?
class BaseType(Node):
    CODE = "60100"
    LABEL = "BaseType"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

    def base(self):
        return self.__children[0]

class TypeQualifier(Node):
    CODE = "50000"
    LABEL = "TypeQualifier"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)

    def qualifier(self):
        return self.__children[0]

# Provides a full type definition
class FullType(Node):
    CODE = "40000"
    LABEL = "FullType"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) >= 2 and len(children) <= 3

        tmp = children.copy()
        self.__qualifier = tmp.pop(0)
        self.__name = tmp.pop(0) if isinstance(tmp[0], TypeName) else None
        self.__base_type = tmp.pop(0) if tmp else None

        assert isinstance(self.__qualifier, TypeQualifier)
        assert self.__name is None or isinstance(self.__name, TypeName)

        super().__init__(pos, length, label, children)
    
    def qualifier(self):
        return self.__qualifier
    def name(self):
        return self.__name
    def base_type(self):
        return self.__base_type

class Storage(Node):
    CODE = "340000"
    LABEL = "Storage"
   
    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) >= 1
        assert any([isinstance(c, GenericString) for c in children])
        super().__init__(pos, length, label, children)

    def classes(self):
        return self.__children
