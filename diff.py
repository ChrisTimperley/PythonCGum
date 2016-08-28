#!/usr/bin/env
import json

class Action(object):
    @staticmethod
    def from_json(jsn):
        return ({
            'insert': Insert,
            'remove': Remove,
            'update': Update,
            'move': Move
        })[jsn['action']].from_json(jsn)

class Move(Action):
    @staticmethod
    def from_json(jsn):
        return Move(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, tree_id, parent_id, position):
        self.__tree_id = tree_id
        self.__parent_id = parent_id
        self.__position = position

    def __str__(self):
        return "MOV(%d, %d, %d)" % \
            (self.__tree_id, self.__parent_id, self.__position)

# Doesn't handle insert root
class Insert(Action):
    @staticmethod
    def from_json(jsn):
        return Insert(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, tree_id, parent_id, position):
        self.__tree_id = tree_id
        self.__parent_id = parent_id
        self.__position = position

    def __str__(self):
        return "INS(%d, %d, %d)" % \
            (self.__tree_id, self.__parent_id, self.__position)

class Remove(Action):
    @staticmethod
    def from_json(jsn):
        return Remove(jsn['parent'])

    def __init__(self, parent_id):
        self.__parent_id = parent_id

    def __str__(self):
        return "DEL(%d)" % self.__parent_id

class Update(Action):
    @staticmethod
    def from_json(jsn):
        return Update(jsn['tree'], jsn['label'])

    def __init__(self, tree_id, label):
        self.__tree_id = tree_id
        self.__label = label

    def __str__(self):
        return "UPD(%d, %s)" % (self.__tree_id, self.__label)

class Diff(object):
    @staticmethod
    def from_file(fn):
        with open(fn, 'r') as f:
            return Diff.from_json(json.load(f))

    @staticmethod
    def from_json(jsn):
        return Diff([Action.from_json(action) for action in jsn])

    def __init__(self, actions):
        self.__actions = actions

    def __str__(self):
        return '\n'.join(map(str, self.__actions))
