from cgum.basic import *

# Represents a C preprocessor statement
class PreprocessorStatement(Node):
    CODE = "450300"
    LABEL = "CppTop"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

    def statement(self):
        return self.__children[0]
    def to_s(self):
        return self.statement().to_s()

class OtherDirective(Node):
    CODE = "400400"
    LABEL = "OtherDirective"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)

    def directive(self):
        return self.__children[0].to_s()
    def to_s(self):
        return self.directive()

class Define(Node):
    CODE = "400100"
    LABEL = "Define"

class DefineFunc(Node):
    CODE = "410100"
    LABEL = "DefineFunc"

class DefineExpr(Nide):
    CODE = "420100"
    LABEL = "DefineExpr"

class IfDefTop(Node):
    CODE = "450400"
    LABEL = "IfdefTop"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], IfDefDirective)
        super().__init__(pos, length, label, children)

    def directive(self):
        return self.__children[0].to_s()
    def to_s(self):
        return self.directive()

class IfDefDirective(Node):
    CODE = "440100"
    LABEL = "IfdefDirective"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)

    def directive(self):
        return self.__children[0].to_s()
    def to_s(self):
        return self.directive()

class Include(Node):
    CODE = "400200"
    LABEL = "Include"
    
    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)

    def file(self):
        return self.__children[0].to_s()
    def to_s(self):
        return self.file()
