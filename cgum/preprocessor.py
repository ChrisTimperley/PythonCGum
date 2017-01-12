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

class MacroDecl(Node):
    CODE = "350200"
    LABEL = "MacroDecl"

class MacroStmt(Node):
    CODE = "260001"
    LABEL = "MacroStmt"

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

# TODO: wtf is this?
class DefineDoWhileZero(Node):
    CODE = "420400"
    LABEL = "DefineDoWhileZero"

class Undef(Node):
    CODE = "410002"
    LABEL = "Undef"

class ActMisc(Node):
    CODE = "30100"
    LABEL = "ActMisc"

class Define(Node):
    CODE = "400100"
    LABEL = "Define"

class DefineMulti(Node):
    CODE = "420700"
    LABEL = "DefineMulti"

class DefineType(Node):
    CODE = "420300"
    LABEL = "DefineType"

class DefineStmt(Node):
    CODE = "420200"
    LABEL = "DefineStmt"

class DefineFunc(Node):
    CODE = "410100"
    LABEL = "DefineFunc"

class DefineExpr(Node):
    CODE = "420100"
    LABEL = "DefineExpr"

class DefineVar(Node):
    CODE = "410001"
    LABEL = "DefineVar"

class DefineEmpty(Node):
    CODE = "420001"
    LABEL = "DefineEmpty"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert children == []
        super().__init__(pos, length, label, children)

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
