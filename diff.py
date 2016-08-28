#!/usr/bin/env
class Action(object):
    
    @staticmethod
    def from_json(jsn):


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

# Remove(NodeID)
class Remove(Object):
    @staticmethod
    def from_json(jsn):
        pass

# Update(
class Update(Object):

class Diff(object):
    def __init__(self, actions):
        self.__actions = actions
