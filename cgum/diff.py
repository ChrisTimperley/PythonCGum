#!/usr/bin/env
from cgum.utility import *
from cgum.program import Program
import codecs
import json
import tempfile
from subprocess import Popen

class Mappings(object):
    @staticmethod
    def from_json(jsn):
        before_to_after = dict()
        after_to_before = dict()
        for m in jsn:
            src = int(m['src'])
            dest = int(m['dest'])
            before_to_after[src] = dest
            after_to_before[dest] = src
        return Mappings(before_to_after, after_to_before)

    def __init__(self, before_to_after, after_to_before):
        self.before_to_after = before_to_after
        self.after_to_before = after_to_before

    # Given the number of a node in P, returns the number of the matching node
    # in P', or None if no such match exists.
    def after(self, num):
        return self.before_to_after.get(num, None)

    # Given the number of a node in P', returns the number of the matching node
    # in P, or None if no such match exists.
    def before(self, num):
        return self.after_to_before.get(num, None)

class Action(object):
    @staticmethod
    def from_json_with_mappings(jsn, mapping):
        return ({
            'insert': Insert,
            'update': Update,
            'move': Move,
            'delete': Delete
        })[jsn['action']].from_json_with_mappings(jsn, mapping)

# Gives the ID of the node in the original tree that was deleted.
class Delete(Action):
    @staticmethod
    def from_json_with_mappings(jsn, mapping):
        return Delete(jsn['tree'])

    def __init__(self, node_id):
        self.__deleted_id = node_id
        self.__deleted = None

    def annotate(self, before, after):
        self.__deleted = before.find(self.__deleted_id)

    # Returns the deleted node from the before AST
    def deleted(self):
        return self.__deleted

    def __str__(self):
        return "DEL(%d)" % self.__deleted_id

# Position parameter is NOT to be trusted
class Move(Action):
    @staticmethod
    def from_json_with_mappings(jsn, mapping):
        from_id = jsn['tree']
        to_id = mapping.after(from_id)
        return Move(from_id, to_id, jsn['parent'], jsn['at'])

    def __init__(self, from_id, to_id, parent_id, position): 
        self.__from_id = from_id
        self.__to_id = to_id
        self.__parent_id = parent_id
        self.__position = position
        self.__from = None
        self.__to = None

    # Annotates this action by recording the from and to nodes
    def annotate(self, before, after):
        self.__from = before.find(self.__from_id)
        self.__to = after.find(self.__to_id)

    # Returns the node in the before AST
    def moved_from(self):
        if self.__from is None:
            raise Exception("moved_from: action hasn't been annotated")
        return self.__from
    # Returns the node in the after AST
    def moved_to(self):
        if self.__to is None:
            raise Exception("moved_to: action hasn't been annotated")
        return self.__to

    # Returns the ID of the node that was moved in the before AST
    def moved_from_id(self):
        return self.__to_id
    def moved_to_id(self):
        return self.__from_id

    # Returns the original (incorrect) GumTree description
    def __str__(self):
        return "MOV(%d, %d, %d)" % \
            (self.__from_id, self.__parent_id, self.__position)

# Doesn't handle insert root?
class Insert(Action):
    @staticmethod
    def from_json_with_mappings(jsn, mapping):
        return Insert(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, inserted_id, parent_id, position):
        self.__inserted_id = inserted_id
        self.__parent_id = parent_id
        self.__position = position
        self.__inserted = None
        self.__parent = None

    # Annotates this action by caching the inserted and parent nodes
    def annotate(self, before, after):
        self.__inserted = after.find(self.__inserted_id)
        self.__parent = after.find(self.__parent_id)

    # Returns the node which was inserted into the AST
    def inserted(self):
        return self.__inserted
    # Returns the parent of the node that was inserted into the AST
    def parent(self):
        return self.__parent
    
    # Returns the ID of the node that was inserted into the AST
    def inserted_id(self):
        return self.__child_id
    def parent_id(self):
        return self.__parent_id
    # Returns the position that the node was inserted into its parents subtree,
    # according to GumTree output; flawed.
    def position(self):
        return self.__position

    def __str__(self):
        return "INS(%d, %d, %d)" % \
            (self.__inserted_id, self.__parent_id, self.__position)

class Update(Action):
    @staticmethod
    def from_json_with_mappings(jsn, mapping):
        after_id = mapping.after(jsn['tree'])
        return Update(jsn['tree'], after_id, jsn['label'])

    def __init__(self, before_id, after_id, label):
        self.__before_id = before_id
        self.__after_id = after_id
        self.__label = label
        self.__before = None
        self.__after = None

    # Annotates this action by caching the before and after forms of the node
    def annotate(self, before, after):
        self.__before = before.find(self.__before_id)
        self.__after = after.find(self.__after_id)

    # Returns the node that was the subject of this Update operation, in P
    def before(self):
        return self.__before
    # Returns the node that was the subject of this Update operation, in P'
    def after(self):
        return self.__after

    # Returns the ID of the node in P
    def before_id(self):
        return self.__before_id
    # Returns the ID of the node in P'
    def after_id(self):
        return self.__after_id
    # Returns the updated label for this node
    def label(self):
        return self.__label

    # Returns a string description of the operation, in its original GumTree
    # encoding
    def __str__(self):
        return "UPD(%d, %s)" % (self.__before_id, self.__label)

class AnnotatedDiff(object):
    @staticmethod
    def from_source_files(fn_from, fn_to):
        tmp_f = tempfile.NamedTemporaryFile()
        AnnotatedDiff.parse_to_json_file(fn_from, fn_to, tmp_f)
        before = Program.from_source_file(fn_from)
        after = Program.from_source_file(fn_to)
        return AnnotatedDiff.from_file(tmp_f.name,\
                                       before,\
                                       after)

    @staticmethod
    def parse_to_json_file(fn_from, fn_to, jsn_fn):
        assert Popen(("gumtree jsondiff \"%s\" \"%s\"" % (fn_from, fn_to)), \
                     shell=True, stdin=FNULL, stdout=jsn_fn).wait() == 0

    @staticmethod
    def from_file(fn, before, after):
        with codecs.open(fn, 'r', 'utf-8') as f:
            return AnnotatedDiff.from_json(json.load(f), before, after)

    @staticmethod
    def from_json(jsn, before, after):
        mappings = Mappings.from_json(jsn['matches'])
        actions = \
            [Action.from_json_with_mappings(a, mappings) for a in jsn['actions']]
        return AnnotatedDiff(actions, mappings, before, after)

    def __init__(self, actions, mappings, before, after):
        self.__actions = actions
        self.__mappings = mappings
        self.__before = before
        self.__after = after

        self.__insertions = []
        self.__deletions = []
        self.__updates = []
        self.__moves = []

        # Annotate and group the actions
        for action in self.__actions:
            action.annotate(before, after)
            ({
                Insert: self.__insertions,
                Delete: self.__deletions,
                Update: self.__updates,
                Move: self.__moves
            })[action.__class__].append(action)

    def before(self):
        return self.__before
    def after(self):
        return self.__after

    def actions(self):
        return self.__actions
    def insertions(self):
        return self.__insertions
    def deletions(self):
        return self.__deletions
    def moves(self):
        return self.__moves
    def updates(self):
        return self.__updates
    def mappings(self):
        return self.__mappings

    # checks whether a given node in P' was moved to that location
    def was_moved_to(self, to):
        return any([to == move.moved_to() in self.moves()])

    # checks whether a given node in P was moved to another location
    def was_moved_from(self, frm):
        return any([frm == move.moved_from() in self.moves()])

    # Given a node in P, return the matching node in P', or None if no such
    # match exists.
    def was_is(self, node):
        assert not node is None, "was_is: provided node must not be null"

        was_num = node.number()
        is_num = self.__mappings.after(was_num)

        if is_num is None:
            return None
        else:
            return self.__after.find(is_num)

    # Given a node in P', return the matching node in P, or None if no such
    # match exists.
    def is_was(self, node):
        assert not node is None, "is_was: provided node must not be null"

        is_num = node.number()
        was_num = self.__mappings.before(is_num)

        if was_num is None:
            return None
        else:
            return self.__before.find(was_num)

    def __str__(self):
        return '\n'.join(map(str, self.__actions))
