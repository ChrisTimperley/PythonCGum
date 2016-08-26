#!/usr/bin/env python3
import os.path
import json
import expression
import statement
import preprocessor
import program
from basic import *

# Parses a JSON CGum AST, stored in a file at a specified location, into an
# equivalent, Python representation
def from_file(fn):
    print("Attempting to read CGum AST from a JSON file: %s" % fn)
    assert os.path.isfile(fn), "file not found"
    with open(fn, 'r') as f:
        Node.from_json(json.load(f)['root'])
    print("Finished converting CGum AST from JSON into Python")

if __name__ == "__main__":

    # Let's try and build an example AST
    from_file("example.cgum.json")
