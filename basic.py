# The base class used by all AST nodes
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

class GenericList(Node):
    CODE = 470000
    LABEL = "GenericList"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == GenericList.CODE
        contents = [Node.from_json(c) for c in jsn['children']]
        return GenericList(jsn['pos'], contents)

    def __init__(self, pos, contents):
        super().__init__(pos)
        self.contents = contents

class GenericString(Node):
    CODE = 480000
    LABEL = "GenericString"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == GenericString.CODE
        return GenericString(jsn['pos'], jsn['label'])

    def __init__(self, pos, contents):
        super().__init__(pos)
        self.__contents = contents
