#!/bin/usr/env python3
#
# Ignores CppTop for now; easy enough to add in later.
#
import json

class Node(object):
    def __init__(self, pos):
        self.pos = pos
    def to_s(self):
        raise NotImplementedError('No `to_s` method exists for this object')
    def to_json(self):
        raise NotImplementedError('No `to_json` method exists for this object')

##
# STATEMENTS
##
class Statement(Node):
    pass

class ExprStatement(Node):
    pass

# 300100 - If
class IfElse(Statement):
    @staticmethod
    def from_json(jsn):
       pass 
    def __init__(self, condition, then, els):
        self.condition = condition
        self.then = then
        self.els = els
    def to_json(self):
        pass

##
# EXPRESSIONS
##
class Expression(Node):
    pass

class Constant(Expression):
    def __init__(self, pos, value):
        super().__init__(pos)
        self.value = value
    def to_s(self):
        return str(self.value)

# 242000 - ParenExpr
class Parentheses(Expression):
    pass

class Binary(Expression):
    pass

class Unary(Expression):
    pass

# 280003 - Return
class Return(Statement):
    pass

##
# PROGRAM
##

# 460000 - Program
class Program(Node):
    pass
