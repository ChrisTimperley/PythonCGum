#!/usr/bin/env python3
import program
import diff

if __name__ == "__main__":

    # Let's try and build an example AST
    print("BEFORE")
    before = program.Program.from_source_file("example/minimal/before.c")
    before.pp()

    print("\nAFTER")
    after = program.Program.from_source_file("example/minimal/after.c")
    after.pp()

    diff = diff.Diff.from_source_files("example/minimal/before.c",\
                                       "example/minimal/after.c")

    print("\nDIFF")
    print(diff)

    diff.correct()
    print("")
    print("CORRECTED")
    print(diff)
