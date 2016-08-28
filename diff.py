#!/usr/bin/env
class Action(object):
    @staticmethod
    def from_json(jsn):
        return ({
            'insert': Insert,
            'remove': Remove,
            'update': Update
        })[jsn['action']].from_jsn(jsn)

# Insert(DonorID, ParentID, Position)
#
# Doesn't handle insert root
class Insert(object):
    @staticmethod
    def from_json(jsn):
        return Add(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, tree_id, parent_id, position):
        self.__tree_id = tree_id
        self.__parent_id = parent_Id
        self.__position = position

class Remove(Object):
    @staticmethod
    def from_json(jsn):
        return Remove(jsn['parent'])

    def __init__(self, parent_id):
        self.__parent_id = parent_id

class Update(Object):
    @staticmethod
    def from_json(jsn):
        return Update(jsn['tree'], jsn['label'])

    def __init__(self, tree_id, label):
        self.__tree_id = tree_id
        self.__label = label

class Diff(object):
    def __init__(self, actions):
        self.__actions = actions
