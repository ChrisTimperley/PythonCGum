#!/usr/bin/env python3
import basic
import expression
import statement
import preprocessor
import program

# This look-up table, initialised upon the first call to `from_json`, maps CGum
# AST types to their representative Python classes, using the type ID.
__CODE_CLASS_LOOKUP = {}

# Constructs the AST class look-up table. Used by `lookup_table` to build the
# look-up table upon its first request.
def __build_lookup_table(typ):
    if hasattr(typ, 'CODE'):
        print("Registering AST type into lookup table [%d]: %s" % (typ.CODE, typ.__name__))
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

# Parses a JSON CGum AST into an equivalent, Python-based C AST
def from_json(jsn):
    pass

if __name__ == "__main__":
    print(lookup_table())
