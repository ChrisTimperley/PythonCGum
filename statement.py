from basic import *
import expression

class Statement(Node):
    pass

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

class For(Statement):
    CODE = "310300"
    LABEL = "For"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], For.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 3
        assert isinstance(children[0], ExprStatement)
        assert isinstance(children[1], ExprStatement)
        assert isinstance(children[2], ExprStatement)
        return For(jsn['pos'], children[0], children[1], children[2])

    def __init__(self, pos, initialisation, condition, after):
        super().__init__(pos)
        self.__initialisation = initialisation
        self.__condition = condition
        self.__after = after

# Never seems to return the result of an expression?
class Return(Statement):
    CODE = "280003"
    LABEL = "Return"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Return.CODE)
        assert not jsn['children']
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
