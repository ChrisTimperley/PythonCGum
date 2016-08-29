from cgum.basic import *

# Represents a C preprocessor statement
class PreprocessorStatement(cgum.basic.Node):
    CODE = "450300"
    LABEL = "CppTop"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], OtherDirective)
        super().__init__(pos, length, label, children)

    def statement(self):
        return self.__children[0]
    def to_s(self):
        return self.statement().to_s()

class OtherDirective(cgum.basic.Node):
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
