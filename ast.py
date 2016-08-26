#!/bin/usr/env python3
#
# Ignores CppTop for now; easy enough to add in later.
#
import json
from basic import *
import expression

##
# STATEMENTS
##
class Statement(basic.Node):
    pass

class ExprStatement(basic.Node):
    pass

# 280003 - Return
class Return(Statement):
    pass

class IfElse(Statement):
    CODE = 300100
    LABEL = "If"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == IfElse.CODE 

        # Build the condition
        condition = Node.from_json(jsn['children'][1])

        # Build the "then" branch. This doesn't always result in a block.
        # TODO: Ensure a block is added?
        then = Node.from_json(jsn['children'][2])

        # Build the "else" branch, if there is one.
        if len(jsn['children']) == 4:
            els = Node.from_json(jsn['children'][3])
        else:
            els = None

        return IfElse(jsn['pos'], condition, then, els)

    def __init__(self, pos, condition, then, els):
        super().__init__(pos)
        self.condition = condition
        self.then = then
        self.els = els

# TODO:
# - Separate declarations
class Block(basic.Node):
    CODE = 330000
    LABEL = "Compound"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == Block.CODE

        statements = jsn['children']
        return Block(jsn['pos'], statements)

    def __init__(self, pos, statements):
        super().__init__(pos)
        self.statements = statements

class FunctionParameter(basic.Node):
    CODE = 220100
    LABEL = "ParameterType"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == FunctionParameter.CODE
        return FunctionParameter(jsn['pos'], jsn['children'][0]['label'])

    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name

class FunctionDefinition(basic.Node):
    CODE = 380000
    LABEL = "Definition"

    @staticmethod
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
        statements = statements.statements

        return FunctionDefinition(jsn['pos'], name, parameters, statements)

    def __init__(self, pos, name, parameters, statements):
        super().__init__(pos)
        self.name = name
        self.parameters = parameters
        self.statements = statements

##
# PROGRAM
##
class Program(basic.Node):
    CODE = 460000
    LABEL = "Program"

    @staticmethod
    def from_json(jsn):
        # These aren't statements - declarations, directives, definitions
        statements = [Node.from_json(s) for s in jsn['children']]
        return Program(jsn['pos'], jsn['length'], statements)

    def __init__(self, pos, value, statements):
        super().__init__(pos, value)
        self.statements = statements

# Register the corresponding CGum type codes for each Node type
