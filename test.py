#!/usr/bin/python3
import cgum.program
import cgum.diff

before = cgum.program.Program.from_source_file("example/hello-world/before.c")
after = cgum.program.Program.from_source_file("example/hello-world/after.c")
diff = cgum.diff.Diff.from_source_files("example/hello-world/before.c",\
                                        "example/hello-world/after.c")

print("BEFORE")
before.pp()
print("\nAFTER")
after.pp()
print("")
print(diff)
print("")

moved = diff.actions()[0]
print("MOVED FROM: %s" % moved.moved_from(before, after).typeLabel())
print("MOVED TO: %s" % moved.moved_to(before, after).typeLabel())
