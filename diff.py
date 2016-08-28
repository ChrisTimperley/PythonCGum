#!/usr/bin/env
import json

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
        self.__parent_id = parent_id

    def parent_id(self):
        return self.__parent_id
    def set_parent_id(self, x):
        self.__parent_id = x
        return x

# Gives the ID of the node in the original tree that was deleted.
# If we want to be able to sequentially generate the edit by applying actions
# then we need to modify this ID to the correct ID at the point of application.
class Delete(Action):
    @staticmethod
    def from_json(jsn):
        return Delete(jsn['tree'])

    # Hmm... Surely this is the same ID?
    def correct(self, map_id):
        return map_id

    def __str__(self):
        return "DEL(%d)" % self.parent_id()

class Move(Action):
    @staticmethod
    def from_json(jsn):
        return Move(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, tree_id, parent_id, position):
        super().__init__(parent_id)
        self.__tree_id = tree_id
        self.__position = position

    # This one may be a little trickier to correct
    def correct(self, id_map):
        return id_map

    def tree_id(self):
        return self.__tree_id
    def position(self):
        return self.__position

    def __str__(self):
        return "MOV(%d, %d, %d)" % \
            (self.tree_id(), self.parent_id(), self.position())

# Doesn't handle insert root
class Insert(Action):
    @staticmethod
    def from_json(jsn):
        return Insert(jsn['tree'], jsn['parent'], jsn['at'])

    def __init__(self, tree_id, parent_id, position):
        super().__init__(parent_id)
        self.__tree_id = tree_id
        self.__position = position

    def correct(self, id_map):
        post_parent_id = self.parent_id()
        id_map[post_parent_id] = \
            self.set_parent_id(id_map[post_parent_id] - 1)
        return id_map

    def tree_id(self):
        return self.__tree_id
    def position(self):
        return self.__position

    def __str__(self):
        return "INS(%d, %d, %d)" % \
            (self.tree_id(), self.parent_id(), self.position())

# TODO: Fix me! I should remove a node from a parent at a given ID
class Remove(Action):
    @staticmethod
    def from_json(jsn):
        assert not ('at' in jsn)
        return Remove(jsn['parent'])

    # Since we only ever seem to remove single nodes, we can correct the ID
    # by adding one.
    def correct(self, id_map):
        post_parent_id = self.__parent_id
        id_map[post_parent_id] = \
            self.set_parent_id(id_map[post_parent_id] + 1)
        return id_map

    def __str__(self):
        return "REM(%d)" % self.parent_id()

class Update(Action):
    @staticmethod
    def from_json(jsn):
        return Update(jsn['tree'], jsn['label'])

    def __init__(self, parent_id, label):
        super().__init__(parent_id)
        self.__label = label

    # Update actions have no effect on the IDs of successive edits
    def correct(self, id_map):
        return id_map

    def label(self):
        return self.__label

    def __str__(self):
        return "UPD(%d, %s)" % (self.parent_id(), self.label())

class Diff(object):
    @staticmethod
    def from_source_files(fn_from, fn_to):
        #with open
        pass

    @staticmethod
    def from_file(fn):
        with open(fn, 'r') as f:
            return Diff.from_json(json.load(f))

    @staticmethod
    def from_json(jsn):
        return Diff([Action.from_json(action) for action in jsn])

    def __init__(self, actions):
        self.__actions = actions

    # Fixes the IDs in the patch, such that a theoretically executable
    # patch is produced
    def correct(self):
        id_map = {}
        for action in reversed(self.__actions):
            parent_id = action.parent_id()
            if not (parent_id in id_map):
                id_map[parent_id] = parent_id
            action.correct(id_map)

    def __str__(self):
        return '\n'.join(map(str, self.__actions))
