#!/usr/bin/env python3
import program
import diff

if __name__ == "__main__":

    # Let's try and build an example AST
    print("BEFORE")
    before = program.Program.from_source_file("example/minimal/before.c")

    print("\nAFTER")
    after = program.Program.from_file("example/minimal/after.cgum.json")
    diff = diff.Diff.from_file("example/minimal/diff.cgum.json")

    print("\nDIFF")
    print(diff)

    diff.correct()
    print("")
    print("CORRECTED")
    print(diff)
