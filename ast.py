#!/bin/usr/env python3
import json

class Node(object):
    def to_s(self):
        raise NotImplementedError('No `to_s` method exists for this object')
    def to_json(self):
        raise NotImplementedError('No `to_json` method exists for this object')

class IfElse(Node):
    @staticmethod
    def from_json(jsn):
       pass 
    def __init__(self, condition, then, els):
        self.condition = condition
        self.then = then
        self.els = els
    def to_json(self):
        pass

class Return(Node):
    pass

class Program(Node):
    pass
