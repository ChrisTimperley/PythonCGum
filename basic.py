# This look-up table, initialised upon the first call to `from_json`, maps CGum
# AST types to their representative Python classes, using the type ID.
__CODE_CLASS_LOOKUP = {}

# Constructs the AST class look-up table. Used by `lookup_table` to build the
# look-up table upon its first request.
def __build_lookup_table(typ):
    if hasattr(typ, 'CODE'):
        #print("Registering AST type [%s]: %s" % (typ.CODE, typ.__name__))
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
    # Constructs an AST node from a given JSON definition
    @staticmethod
    def from_json(jsn):
        assert 'type' in jsn, "expected 'type' property in AST node"
        typid = jsn['type']
        try:
            typ = lookup_table()[typid]
        except KeyError as e:
            raise Exception(("no Python representation of AST node with type %s found." +\
                             "Has CGum type label: %s.") % (typid, jsn['typeLabel']))
        #print("Converting AST node of (Python) type: %s" % typ.__name__)

        # Build the children of this node, if there are any, then extract any
        # attached label
        children = [Node.from_json(c) for c in jsn['children']]
        label = jsn['label'] if 'label' in jsn else None

        # Construct a node of the correct type, using the extracted information
        return typ(jsn['pos'], jsn['length'], label, children)

    def __init__(self, pos, length, label, children):
        self.__pos = int(pos)
        self.__length = int(length)
        self.__label = label
        self.__children = children
        self.__number = None
        self.__depth = None
        self.__size = None

    def label(self):
        return self.__label
    def pos(self):
        return self.__pos
    def length(self):
        return self.__length
    def children(self):
        return self.__children
    def number(self):
        return self.__number
    def size(self):
        return self.__size
    def depth(self):
        return self.__depth

    # Returns the CGum AST type label for this node
    def typeLabel(self):
        return self.__class__.LABEL

    # Recursively renumbers all nodes belonging to the sub-tree rooted at this
    # node. Numbers start at zero. Unfortunately necessary, since the CGum AST
    # output doesn't provide node numbers.
    #
    # FIX: Changed to post-order assignment
    def renumber(self, num=0):
        for c in self.__children:
            num = c.renumber(num)
        print("Assigning number %d to %s at %d" % (num, self.typeLabel(), self.__pos))
        self.__number = num
        return num + 1

    def to_s(self):
        raise NotImplementedError('No `to_s` method exists for this object')
    def to_json(self):
        raise NotImplementedError('No `to_json` method exists for this object')

class Token(Node):
    def __init__(self, pos, length, label, children):
        assert not children
        assert not label
        super().__init__(pos, length, label, children)

class GenericList(Node):
    CODE = "470000"
    LABEL = "GenericList"

    def contents(self):
        return self.__children

class GenericString(Node):
    CODE = "480000"
    LABEL = "GenericString"

    def read(self):
        return self.label()
    def to_s(self):
        return self.label()

# :-(
class NotParsedCorrectly(Node):
    CODE = "450700"
    LABEL = "NotParsedCorrectly"

# I really have no idea what the point of this node is? Seems to contain nodes
# whose presence is otherwise optional. In the case those nodes are missing, a
# None can be found instead.
# From observation, it only ever seems to contain one item, followed by a ;
class Some(Node):
    CODE = "290100"
    LABEL = "Some"

# Strangely, None can have children
class NoneNode(Node):
    CODE = "290001"
    LABEL = "None"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        assert isinstance(children[0], GenericString)
        super().__init__(pos, length, label, children)

# Equally, I have no idea what the Left node is for?
class Left(Node):
    CODE = "20100"
    LABEL = "Left"

    def __init__(self, pos, length, label, children):
        assert label is None
        assert len(children) == 1
        super().__init__(pos, length, label, children)
