# PyCGum
A Python implementation of the CGum AST

## Usage

Generate a CGum AST for a given file as shown below:

```
program = Program.from_source_file("example.c")
```

Alternatively, an AST may be produced from a GumTree JSON AST output file,
produced using `gumtree parse example.c`.

```
program = Program.from_gumtree_file("example.gumtree.json")
```

ASTs, or even partial sub-trees may be loaded manually using the method shown
below, where `jsn` is a JSON file loaded into a Dict object.

```
node = Node.from_json(jsn)
program = Program.from_json(jsn)
```
