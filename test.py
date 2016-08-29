#!/usr/bin/python3
import cgum.program

prog = cgum.program.Program.from_source_file("example/minimal/before.c")

prog.pp()

ret = prog.find(12)

for ancestor in ret.ancestors():
    print(ancestor.typeLabel())
