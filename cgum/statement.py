from cgum.basic import *
import cgum.expression as expression

# Mix-in implemented by all statement types
class Statement(object):
    def is_statement(self):
        return True
    def nearestStmt(self):
        return self

# TODO: Understand this better
class StatementExpression(Node, Statement, expression.Expression):
    CODE = "241800"
    LABEL = "StatementExpr"

    def __init__(self, pos, length, label, children):
        assert label is None
        super().__init__(pos, length, label, children)

# For now, declarations are statements
class DeclarationList(Node, Statement):
    CODE = "350100"
    LABEL = "DeclList"

    def __init__(self, pos, length, label, children):
        assert label is None
        super().__init__(pos, length, label, children)

    def declarations(self):
        return self.__children

# A declaration isn't quite a statement, but this is the best place for it,
# for now.
class Declaration(Node):
    CODE = "450100"
    LABEL = "Declaration"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], DeclarationList)
        super().__init__(pos, length, label, children)

    def declarations(self):
        return self.__children[0]

# Generic definition class
class Definition(Node, Statement):
    CODE = "450200"
    LABEL = "Definition"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

    def defined(self):
        return self.__children[0]

    def to_s(self):
        return self.defined().to_s()

class Goto(Node, Statement):
    CODE = "280100"
    LABEL = "Goto"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)

    def destination(self):
        return self.__children[0]

    def to_s(self):
        return "goto %s" % self.destination()

class Continue(Token, Statement):
    CODE = "280001"
    LABEL = "Continue"

    def to_s(self):
        return "continue"

# Used to specify the default switch case
class Default(Node, Statement):
    CODE = "270400"
    LABEL = "Default"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

class Case(Node, Statement):
    CODE = "270200"
    LABEL = "Case"

    def __init__(self, pos, length, label, children):
        assert len(children) == 2
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]
    def stmt(self):
        return self.__children[1]

class Switch(Node, Statement):
    CODE = "300200"
    LABEL = "Switch"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        assert isinstance(children[1], Block)
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]
    def block(self):
        return self.__children[1]

class Break(Token, Statement):
    CODE = "280002"
    LABEL = "Break"
    def to_s(self):
        return "break"

class ExprStatement(Node, Statement):
    CODE = "260300"
    LABEL = "ExprStatement"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]

class DoWhile(Node, Statement):
    CODE = "310200"
    LABEL = "DoWhile"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        super().__init__(pos, length, label, children)

    def condition(self):
        return self.__children[1]
    def do(self):
        return self.__children[0]

class While(Node, Statement):
    CODE = "310100"
    LABEL = "While"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        super().__init__(pos, length, label, children)

    def condition(self):
        return self.__children[0]
    def do(self):
        return self.__children[1]

class For(Node, Statement):
    CODE = "310300"
    LABEL = "For"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 4
        #assert isinstance(children[0], ExprStatement)
        #assert isinstance(children[1], ExprStatement)
        #assert isinstance(children[2], ExprStatement)
        #assert isinstance(children[3], Block)
        super().__init__(pos, length, label, children)

    def initialisation(self):
        return self.__children[0]
    def condition(self):
        return self.__children[1]
    def after(self):
        return self.__children[2]
    def block(self):
        return self.__children[3]

class ReturnExpr(Node, Statement):
    CODE = "280200"
    LABEL = "ReturnExpr"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]

    def to_s(self):
        return "return %s" % self.__expr.to_s()

class Return(Token, Statement):
    CODE = "280003"
    LABEL = "Return"
    def to_s(self):
        return "return"

# Todo: move to tokens package?
class IfToken(Token):
    CODE = "490100"
    LABEL = "IfToken"

class IfElse(Node, Statement):
    CODE = "300100"
    LABEL = "If"

    def __init__(self, pos, length, label, children):
        assert len(children) >= 3 and len(children) <= 4
        assert isinstance(children[0], IfToken)
        super().__init__(pos, length, label, children)

    def condition(self):
        return self.__children[1]
    def then(self):
        return self.__children[2]
    def els(self):
        return self.__children[3] if len(children) == 4 else None

class Block(Node):
    CODE = "330000"
    LABEL = "Compound"

    def contents(self):
        return self.__children
