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
