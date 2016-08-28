#!/usr/bin/env python3
import os.path
import json
import expression
import statement
import preprocessor
import types
import program
import diff
from basic import *

# Parses a JSON CGum AST, stored in a file at a specified location, into an
# equivalent, Python representation
def from_file(fn):
    print("Attempting to read CGum AST from a JSON file: %s" % fn)
    assert os.path.isfile(fn), "file not found"
    with open(fn, 'r') as f:
        program = Node.from_json(json.load(f)['root'])
    print("Finished converting CGum AST from JSON into Python")
    print("Performing node renumbering...")
    program.renumber()
    print("Finishing node renumbering")

if __name__ == "__main__":

    # Let's try and build an example AST
    before = from_file("example/for-loop/before.cgum.json")
    after = from_file("example/for-loop/after.cgum.json")
    diff = diff.Diff.from_file("example/for-loop/diff.cgum.json")

    print(diff)
