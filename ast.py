#!/bin/usr/env python3
#
# Ignores CppTop for now; easy enough to add in later.
#
import json
from basic import *
import expression
import statement

class Program(Node):
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
