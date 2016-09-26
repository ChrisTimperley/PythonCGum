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
        self.__numberStart = None
        self.__parent = None

    # Determines whether this node is equivalent to a given node.
    def equivalent(self, other):
        return  type(self) == type(other) and\
                self.__label == other.label() and\
                len(self.__children) == len(other.children()) and\
                all([c1.equivalent(c2) for (c1, c2) in zip(self.__children, other.children())])

    # By default nodes are not statements, unless overridden by another class.
    def is_statement(self):
        return False

    def parent(self):
        return self.__parent
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
    def numberRange(self):
        return (self.__numberStart, self.__number)
    def size(self):
        return self.__size
    def depth(self):
        return self.__depth
    def child(self, i):
        return self.__children[i]

    # Returns a list of all the descendants of this node, in order from nearest
    # to furthest.
    def descendants(self):
        return reduce(lambda d, c: d + [c] + c.descendants,\
                      self.__children,\
                      [])

    # Returns a list of all the ancestors of this node, in order from nearest
    # to furthest.
    def ancestors(self):
        if self.__parent:
            return [self.__parent] + self.__parent.ancestors()
        else:
            return []

    # Returns the nearest statement to this node.
    # By default, we find the nearest statement to the parent node, if there
    # is one. If not, None is returned.
    # Statements implement a different nearestStmt, which returns the statement
    # in question.
    def nearestStmt(self):
        return self.__parent.nearestStmt() if self.__parent else None

    # Returns the index of the range that a given node belongs to, or None if
    # it belongs to none of them.
    def __find_helper(self, num, ranges, mn, mx):
        if mx < mn:
            return -1
        pivot = (mn + mx) // 2
        (num_start, num_end) = ranges[pivot]
        if num < num_start:
            return self.__find_helper(num, ranges, mn, pivot - 1)
        elif num > num_end:
            return self.__find_helper(num, ranges, pivot + 1, mx)
        else:
            return pivot

    # Finds a node with a given number within the sub-tree rooted at this node
    def find(self, num):
        if self.__number == num:
            return self
        ind = self.__find_helper(num,\
                                 [c.numberRange() for c in self.__children],\
                                 0, len(self.__children) - 1)
        return self.__children[ind].find(num) if ind >= 0 else None

    # Returns the node of the function that this node belongs to, or None if it
    # doesn't belong to a function (i.e. it's a top-level statement).

    # Pretty-prints the tree rooted at this node; useful for debugging
    def pp(self, depth=0):
        print("%s%s - %d" % ((" " * depth), self.__class__.__name__, self.__number))
        depth += 2
        for c in self.__children:
            c.pp(depth=depth)

    # Returns the CGum AST type label for this node
    def typeLabel(self):
        return self.__class__.LABEL

    # Recursively renumbers all nodes belonging to the sub-tree rooted at this
    # node. Numbers start at zero. Unfortunately necessary, since the CGum AST
    # output doesn't provide node numbers.
    def renumber(self, num=0, parent=None):
        self.__numberStart = num
        self.__parent = parent
        for c in self.__children:
            num = c.renumber(num, self)
        #print("Assigning number %d to %s at %d" % (num, self.typeLabel(), self.__pos))
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
