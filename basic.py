# The base class used by all AST nodes
class Node(object):

    # Syntatic sugar for "from_json" method in "parse" module, relies on the
    # parse module having been loaded, of course. We could get round this, but
    # the system is fairly neat and more than good enough.
    @staticmethod
    def from_json(jsn):
        return parse.from_json(jsn)

    # Compares the code of a JSON AST object against the code expected by the
    # Python class it has been passed to. Nice for debugging. Converts the
    # actual code into an integer for the check
    @staticmethod
    def check_code(actual, expected):
        assert actual == expected,\
            ("actual (%s) and expected (%s) AST type codes didn't match." % (actual, expected))

    def __init__(self, pos):
        self.pos = pos
    def to_s(self):
        raise NotImplementedError('No `to_s` method exists for this object')
    def to_json(self):
        raise NotImplementedError('No `to_json` method exists for this object')

class GenericList(Node):
    CODE = "470000"
    LABEL = "GenericList"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == GenericList.CODE
        contents = [Node.from_json(c) for c in jsn['children']]
        return GenericList(jsn['pos'], contents)

    def __init__(self, pos, contents):
        super().__init__(pos)
        self.__contents = contents

    def contents(self):
        return self.__contents

class GenericString(Node):
    CODE = "480000"
    LABEL = "GenericString"

    @staticmethod
    def from_json(jsn):
        assert jsn['type'] == GenericString.CODE
        return GenericString(jsn['pos'], jsn['label'])

    def __init__(self, pos, contents):
        super().__init__(pos)
        self.__contents = contents

    def read(self):
        return self.__contents

    def to_s(self):
        return self.__contents

# I really have no idea what the point of this node is?
# From observation, it only ever seems to contain one item, followed by a ;
class Some(Node):
    pass

# Equally, I have no idea what the Left node is for?
class Left(Node):
    pass
