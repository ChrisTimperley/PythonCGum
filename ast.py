#!/bin/usr/env python3
#
# Ignores CppTop for now; easy enough to add in later.
#
import json

class Node(object):
    @staticmethod
    def from_json(jsn):
        # Need to build a map of codes -> classes, cache as private static var
        raise NotImplementedError('Not implemented, yet!')

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
        condition = Node.from_json(jsn['children'][0])


        IfElse(jsn['location'], jsn['size'])

    def __init__(self, pos, size, condition, then, els):
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

# 241100 - Binary
class Binary(Expression):
    pass

class Unary(Expression):
    pass

# 280003 - Return
class Return(Statement):
    pass

class FunctionParameter(Node):
    CODE = 220100
    LABEL = "ParameterType"

    def from_json(jsn):
        assert jsn['type'] == FunctionParameter.CODE
        return FunctionParameter(jsn['pos'], jsn['children'][0]['label'])

    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name

class FunctionDefinition(Node):
    CODE = 380000
    LABEL = "Definition"

    def from_json(jsn):
        assert jsn['type'] == FunctionDefinition.CODE

        # Fetch the name
        name = jsn['children'][1]['label']
        
        # Build the parameters
        parameters = jsn['children'][0]
        assert parameters['typeLabel'] == 'ParamList',\
            "expected first child of Definition to be ParamList"
        parameters = parameters['children']
        parameters = [FunctionParameter.from_json(c) for c in parameters]

        # Build the statements
        statements = Block.from_json(jsn['children'][2])
        statements = statements.contents()

        return FunctionDefinition(jsn['pos'], name, parameters, statements)

    def __init__(self, pos, name, parameters, statements):
        super().__init__(pos)
        self.name = name
        self.parameters = parameters
        self.statements = statements

##
# PROGRAM
##
class Program(Node):
    CODE = 460000
    LABEL = "Program"

    def from_json(jsn):
        # These aren't statements - declarations, directives, definitions
        statements = [Node.from_json(s) for s in jsn['children']]
        return Program(jsn['pos'], jsn['length'], statements)

    def __init__(self, pos, value, statements):
        super().__init__(pos, value)
        self.statements = statements

# Register the corresponding CGum type codes for each Node type
