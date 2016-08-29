from cgum.basic import *

# Base class used by all AST nodes deemed to represent a C expression
class Expression(Node):
    pass

class Sequence(Expression):
    CODE = "240600"
    LABEL = "Sequence"

    def expressions(self):
        return self.children()

class RecordAccess(Expression):
    CODE = "241300"
    LABEL = "RecordAccess"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        assert isinstance(children[1], GenericString)
        super().__init__(pos, length, label, children)

    def record(self):
        return self.__children[0]
    def member(self):
        return self.__children[1]

class ArrayAccess(Expression):
    CODE = "241200"
    LABEL = "ArrayAccess"

    def __init__(self, pos, length, label, children):
        assert len(children) == 2
        super().__init__(pos, length, label, children)

    def array(self):
        return self.__children[0]
    def index(self):
        return self.__children[1]

# Not entirely sure what this is meant to be?
# It has no children, so either it ignores the type whose size it measures, or
# it does something entirely different.
class SizeOfType(Token, Expression):
    CODE = "241600"
    LABEL = "SizeOfType"

class Assignment(Expression):
    CODE = "240700"
    LABEL = "Assignment"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 3
        assert isinstance(children[1], GenericString)
        super().__init__(pos, length, label, children)

    def lhs(self):
        return self.__children[0]
    def rhs(self):
        return self.__children[2]

# This seems to just represent Postfix expressions? This has nothing to do with
# Infix expression?
class Infix(Expression):
    CODE = "240900"
    LABEL = "Infix"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        assert isinstance(children[1], GenericString)
        super().__init__(pos, length, label, children)

    def operand(self):
        return self.__children[0]
    def operator(self):
        return self.__children[1]

class Postfix(Expression):
    CODE = "240800"
    LABEL = "Postfix"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        assert isinstance(children[1], GenericString)
        super().__init__(pos, length, label, children)

    def operand(self):
        return self.__children[0]
    def operator(self):
        return self.__children[1]

class RecordPtAccess(Expression):
    CODE = "241400"
    LABEL = "RecordPtAccess"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        assert isinstance(children[1], GenericString)
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]
    def member(self):
        return self.__children[1]

class Identity(Expression):
    CODE = "240100"
    LABEL = "Ident"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)

    def of(self):
        return self.__childen[0].read()
    def to_s(self):
        return self.of()

class Constant(Expression):
    CODE = "240200"
    LABEL = "Constant"

    def __init__(self, pos, length, label, children):
        assert not children
        assert isinstance(label, str)
        super().__init__(pos, length, label, children)

    def value(self):
        return self.__label
    def to_s(self):
        return self.__label

class Cast(Expression):
    CODE = "241700"
    LABEL = "Cast"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]
    def to_s(self):
        return "(UNKNOWN_TYPE) %s" % self.expr().to_s()

# What is the difference between Init and Assignment?
class InitExpr(Expression):
    CODE = "360100"
    LABEL = "InitExpr"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

class Ternary(Expression):
    CODE = "240500"
    LABEL = "CondExpr"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 3
        super().__init__(pos, length, label, children)

    def condition(self):
        return self.__children[0]
    def then(self):
        return self.__children[1]
    def els(self):
        return self.__children[2]

class FunctionCall(Expression):
    CODE = "240400"
    LABEL = "FunCall"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        assert isinstance(children[1], GenericList)
        super().__init__(pos, length, label, children)

    def function(self):
        return self.__children[0]
    def arguments(self): # For now we still go through the GenericList
        return self.__children[1]
    def function_name(self):
        return self.function().to_s()

class Parentheses(Expression):
    CODE = "242000"
    LABEL = "ParenExpr"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]

    def to_s(self):
        return "(%s)" % self.expr().to_s()

# I really have no idea what the point of this node is? Seems to contain nodes
# whose presence is otherwise optional. In the case those nodes are missing, a
# None can be found instead.
# From observation, it only ever seems to contain one item, followed by a ;
class Some(Node):
    CODE = "290100"
    LABEL = "Some"

    def __init__(self, pos, length, label, children):
        assert len(children) <= 2
        assert len(children) == 1 or \
            (isinstance(children[1], GenericString) and (children[1].to_s() == ";"))
        super().__init__(pos, length, label, children)

    def expr(self):
        return self.__children[0]

class Unary(Expression):
    CODE = "241000"
    LABEL = "Unary"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 2
        assert isinstance(children[1], GenericString)
        super().__init__(pos, length, label, children)

    def operand(self):
        return self.__children[0]
    def operator(self):
        return self.__children[1]

class Binary(Expression):
    CODE = "241100"
    LABEL = "Binary"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 3
        assert isinstance(children[1], GenericString)
        super().__init__(pos, length, label, children)

    def lhs(self):
        return self.__children[0]
    def op(self):
        return self.__children[1].to_s()
    def rhs(self):
        return self.__children[2]

# TODO: Returns the result of an expression; should be a statement?
class ReturnExpr(Expression):
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
