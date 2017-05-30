payasm
======

A sweet little python assembler which assembles back output from `dis` to python bytecode.

##What it can do?

payASM can assemble your disassembled python code into CPython's bytecode implementation. So,
you can write the assembled bytecode as a `pyc` file and execute it with a Python interpreter.

Currently the test suite contains a simple `Hello World!` program and an Armstrong number
generator program. More test cases with complex disassemblies are welcome.

This project is a work-in-progress. So, there is a huge  number of limitations.

##Limitations

 - Currently works only with Python 2. (Although extending it to Python3 is trivial)
 - No support for lambdas
 - No ************`*args` and `**kwargs` support

##Contributions

Contributions are welcome :smile:
