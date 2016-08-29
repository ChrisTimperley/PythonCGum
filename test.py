#!/usr/bin/python3
import cgum.program

prog = cgum.program.Program.from_source_file("example/minimal/before.c")

prog.pp()

print(prog.find(12).typeLabel())
