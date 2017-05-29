import unittest
from subprocess import check_output
import os
from payasm import payasm

class PayasmTest(unittest.TestCase):
    """Tests for payasm assembler"""

    def test_hello_world(self):
        filename = "tests/disasm-hello-world"
        with open(filename, 'r') as fp:
            disasm = fp.read()
            payasm.assemble(disasm, "tests/hello-world")
    
        output = check_output(['python2', 'tests/hello-world.pyc'])
        self.assertEqual("Hello World!\n", output)
     

