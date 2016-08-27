# This look-up table, initialised upon the first call to `from_json`, maps CGum
# AST types to their representative Python classes, using the type ID.
__CODE_CLASS_LOOKUP = {}

# Constructs the AST class look-up table. Used by `lookup_table` to build the
# look-up table upon its first request.
def __build_lookup_table(typ):
    if hasattr(typ, 'CODE'):
        print("Registering AST type [%s]: %s" % (typ.CODE, typ.__name__))
        __CODE_CLASS_LOOKUP[typ.CODE] = typ
    for sub_typ in typ.__subclasses__():
        __build_lookup_table(sub_typ)

# Used to return the type ID to Python class look-up table.
# Responsible for overseeing the construction of the look-up table on its first
# invocation.
def lookup_table():
    if not __CODE_CLASS_LOOKUP:
        __build_lookup_table(Node)
    return __CODE_CLASS_LOOKUP

# The base class used by all AST nodes
class Node(object):

    # Syntatic sugar for "from_json" method in "parse" module, relies on the
    # parse module having been loaded, of course. We could get round this, but
    # the system is fairly neat and more than good enough.
    @staticmethod
    def from_json(jsn):
        assert 'type' in jsn, "expected 'type' property in AST node"
        typid = jsn['type']
        try:
            typ = lookup_table()[typid]
        except KeyError as e:
            raise Exception(("no Python representation of AST node with type %s found." +\
                             "Has CGum type label: %s.") % (typid, jsn['typeLabel']))
        print("Converting AST node of (Python) type: %s" % typ.__name__)

        try:
            return typ.from_json(jsn)
        except Exception as e:
            raise Exception("Failed to convert AST node at position %s. Reason: %s"\
                            % (jsn['pos'], str(e)))

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
        Node.check_code(jsn['type'], GenericString.CODE)
        assert jsn['type'] == GenericString.CODE
        return GenericString(jsn['pos'], jsn['label'])

    def __init__(self, pos, contents):
        super().__init__(pos)
        self.__contents = contents

    def read(self):
        return self.__contents

    def to_s(self):
        return self.__contents

# :-(
class NotParsedCorrectly(Node):
    CODE = "450700"
    LABEL = "NotParsedCorrectly"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], NotParsedCorrectly.CODE)
        return NotParsedCorrectly(jsn['pos'],\
                                  [Node.from_json(c) for c in jsn['children']])

    def __init__(self, pos, children):
        super().__init__(pos)
        self.__children = children

# I really have no idea what the point of this node is?
# From observation, it only ever seems to contain one item, followed by a ;
class Some(Node):
    pass

# Strangely, None can have children
class NoneNode(Node):
    CODE = "290001"
    LABEL = "None"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], NoneNode.CODE)
        children = [Node.from_json(c) for c in jsn['children']]
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        return NoneNode(jsn['pos'], children[0])

    def __init__(self, pos, string):
        super().__init__(pos)
        self.__string = string

# Equally, I have no idea what the Left node is for?
class Left(Node):
    CODE = "20100"
    LABEL = "Left"

    @staticmethod
    def from_json(jsn):
        Node.check_code(jsn['type'], Left.CODE)
        assert len(jsn['children']) == 1
        return Left(jsn['pos'], Node.from_json(jsn['children'][0]))

    def __init__(self, pos, left):
        super().__init__(pos)
        self.__left = left
