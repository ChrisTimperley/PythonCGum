#!/usr/bin/env
#
# TODO:
# Use mappings to inform construction and to avoid problems in GumTree's diff
# encodings
#
from cgum.utility import *
import json
import tempfile
from subprocess import Popen

class Action(object):
    @staticmethod
    def from_json(jsn):
        return ({
            'insert': Insert,
            'remove': Remove,
            'update': Update,
            'move': Move,
            'delete': Delete
        })[jsn['action']].from_json(jsn)

    def __init__(self, parent_id):
        self.__parent_id = int(parent_id)

    def parent_id(self):
        return self.__parent_id
    def set_parent_id(self, x):
        self.__parent_id = x
        return x

# Gives the ID of the node in the original tree that was deleted.
class Delete(Action):
    @staticmethod
    def from_json(jsn):
        return Delete(jsn['tree'])

    # Returns the deleted node from the before AST
    def deleted(self, before, after):
        return before.find(self.parent_id())

    def __str__(self):
        return "DEL(%d)" % self.parent_id()

class Move(Action):
    @staticmethod
    def from_json(jsn):
        return Move(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, tree_id, parent_id, position):
        #assert position > 0
        super().__init__(parent_id)
        self.__tree_id = tree_id
        self.__position = position

    # Annotates this action by recording the from and to nodes
    def annotate(self, before, after):
        self.__moved_from = before.find(self.moved_from_id())
        self.__moved_to = after.find(self.moved_to_id())

    # Returns the node in the before AST
    def moved_from(self):
        if self.__moved_from is None:
            raise Exception("moved_from: action hasn't been annotated")
        return self.__moved_from
    # Returns the node in the after AST
    def moved_to(self):
        if self.__moved_to is None:
            raise Exception("moved_to: action hasn't been annotated")
        return self.__moved_to

    # Returns the ID of the node that was moved in the before AST
    def moved_from_id(self):
        return self.__moved_to_id
    def moved_to_id(self):
        return self.__moved_from_id

    #def __str__(self):
    #    return "MOV(%d, %d, %d)" % \
    #        (self.tree_id(), self.parent_id(), self.position())

# Doesn't handle insert root
class Insert(Action):
    @staticmethod
    def from_json(jsn):
        return Insert(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, child_id, parent_id, position):
        super().__init__(parent_id)
        self.__child_id = child_id
        self.__position = position

    # Returns the node which was inserted into the AST
    def inserted(self, before, after):
        return after.find(self.__child_id)

    def child_id(self):
        return self.__child_id
    def set_child_id(self, x):
        self.__child_id = x
    def position(self):
        return self.__position

    def __str__(self):
        return "INS(%d, %d, %d)" % \
            (self.child_id(), self.parent_id(), self.position())

class Remove(Action):
    @staticmethod
    def from_json(jsn):
        assert not ('at' in jsn)
        return Remove(jsn['parent'])

    # Returns the node which was removed from the before AST
    def removed(self, before, after):
        raise NotImplementedError("Look into how removal indices work")

    def __str__(self):
        return "REM(%d)" % self.parent_id()

class Update(Action):
    @staticmethod
    def from_json(jsn):
        return Update(jsn['tree'], jsn['label'])

    def __init__(self, parent_id, label):
        super().__init__(parent_id)
        self.__label = label

    # Returns the node that was updated by this operation (within the
    # original tree)
    def updated(self, before, after):
        before.find(self.parent_id())

    def label(self):
        return self.__label

    def __str__(self):
        return "UPD(%d, %s)" % (self.parent_id(), self.label())

class Diff(object):
    @staticmethod
    def from_source_files(fn_from, fn_to):
        tmp_f = tempfile.NamedTemporaryFile()
        assert Popen(("gumtree jsondiff \"%s\" \"%s\"" % (fn_from, fn_to)), \
                     shell=True, stdin=FNULL, stdout=tmp_f).wait() == 0
        return Diff.from_file(tmp_f.name)

    @staticmethod
    def from_file(fn):
        with open(fn, 'r') as f:
            return Diff.from_json(json.load(f))

    @staticmethod
    def from_json(jsn):
        return Diff([Action.from_json(action) for action in jsn])

    def __init__(self, actions):
        self.__actions = actions
        self.__insertions = []
        self.__deletions = []
        self.__removals = []
        self.__updates = []
        self.__moves = []
        for action in self.__actions:
            ({
                Insert: self.__insertions,
                Delete: self.__deletions,
                Remove: self.__removals,
                Update: self.__updates,
                Move: self.__moves
            })[action.__class__].append(action)

    def actions(self):
        return self.__actions
    def insertions(self):
        return self.__insertions
    def deletions(self):
        return self.__deletions
    def removals(self):
        return self.__removals
    def moves(self):
        return self.__moves
    def updates(self):
        return self.__updates

    def __str__(self):
        return '\n'.join(map(str, self.__actions))
