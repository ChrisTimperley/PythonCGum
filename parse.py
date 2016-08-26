#!/usr/bin/env python3
import os.path
import json
import basic
import expression
import statement
import preprocessor
import program

# This look-up table, initialised upon the first call to `from_json`, maps CGum
# AST types to their representative Python classes, using the type ID.
__CODE_CLASS_LOOKUP = {}

# Debugging flag
__DEBUGGING = True

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
        __build_lookup_table(basic.Node)
    return __CODE_CLASS_LOOKUP

# Parses a JSON CGum AST into an equivalent, Python representation
def from_json(jsn):
    assert 'type' in jsn, "expected 'type' property in AST node"
    typid = jsn['type']
    try:
        typ = lookup_table()[typid]
    except KeyError as e:
        raise Exception("no Python representation of AST node with type %d found" % typid)
    print("Converting AST node of (Python) type: %s" % typ.__name__)
    return typ.from_json(jsn)

# Parses a JSON CGum AST, stored in a file at a specified location, into an
# equivalent, Python representation
def from_file(fn):
    print("Attempting to read CGum AST from a JSON file: %s" % fn)
    assert os.path.isfile(fn), "file not found"
    with open(fn, 'r') as f:
        from_json(json.load(f)['root'])
    print("Finished converting CGum AST from JSON into Python")

if __name__ == "__main__":

    # Let's try and build an example AST
    from_file("example.cgum.json")
