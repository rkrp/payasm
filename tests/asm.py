import unittest
from subprocess import check_output
from payasm import payasm

class PayasmTest(unittest.TestCase):
    """Tests for payasm assembler"""

    def test_hello_world(self):
        filename = "tests/disasm-hello-world"
        with open(filename, 'r') as fp:
            disasm = fp.read()
        instructions = payasm.parse_instructions(disasm)
        code = payasm.assemble(instructions, "tests/hello-world")
        payasm.write_pyc(code, "tests/hello-world.pyc")

        output = check_output(['python2', 'tests/hello-world.pyc'])
        self.assertEqual("Hello World!\n", output)

    def test_armstrong(self):
        filename = "tests/disasm_simple_armstrong"
        with open(filename, 'r') as fp:
            disasm = fp.read()
        instructions = payasm.parse_instructions(disasm)
        payasm.assemble(instructions, "tests/simple_armstrong")

