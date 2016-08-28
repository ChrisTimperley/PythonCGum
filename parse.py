#!/usr/bin/env python3
import os.path
from program import Program
import diff

if __name__ == "__main__":

    # Let's try and build an example AST
    print("BEFORE")
    before = Program.from_file("example/minimal/before.cgum.json")

    print("\nAFTER")
    after = Program.from_file("example/minimal/after.cgum.json")
    diff = diff.Diff.from_file("example/minimal/diff.cgum.json")

    print("\nDIFF")
    print(diff)

    diff.correct()
    print("")
    print("CORRECTED")
    print(diff)
