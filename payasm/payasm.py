#!/usr/bin/python2

import opcode
from types import CodeType
import struct
import marshal

class Instruction:
    def __init__(self, inst):
        self.raw = inst
        inst = inst.split()
        self.opcode = inst[0]
        self.opbyte = opcode.opmap[self.opcode]

        #Check if the instruction has arguments
        self.has_arg = self.opbyte >= 0x5a

        if self.has_arg:
            self.arg = int(inst[1])
            try:
                self.arg_val = inst[2]
            except KeyError:
                pass

    def __repr__(self):
        return self.raw


WHITESPACE_LEN = 16

def get_constants(inst):
    return (inst.arg, inst.arg_val)

def populate_args(inst):
    if inst.has_arg:
        return struct.pack('H', inst.arg)
    else:
        return ''


def assemble(disasm, target_name):
    code = ''
    insts = [inst[WHITESPACE_LEN:] for inst in disasm.split("\n")]

    constants = {}
    for inst in insts:
        if inst.strip() == '':
            continue
        inst = Instruction(inst)

        #Generating bytecode
        code += chr(inst.opbyte)
        code += populate_args(inst)

        #Add possible constants
        if inst.opcode == 'LOAD_CONST':
            index, value = get_constants(inst)
            constants[index] = value

    n_constants = max(constants)
    const_list = []
    try:
        i = 0
        while True:
            const_list.append(constants[i])
            i += 1
    except KeyError:
            pass
    print const_list
    print len(code)
    """
    code_type = CodeType(
        0,          #argcount
        0,          #kwargcount
        nlocals,
        100,        #hardcoded as 100
        flags,
        code,       #bytecode
        const_list, #list of constants
        names,
        varnames,
        filename,
        name,
        firstlineno,
        lnotab,
        freevars,
        cellvars,
    )
    """

    #write_pyc(code_type, target_name + ".pyc")

def write_pyc(code, location):
    py_magic = '\x03\xf3\x0d\x0a'
    mod_time = '\xe9\xf5\x29\x59'
    pyc = py_magic + mod_time + code
    with open(location, 'w') as f:
        f.write(pyc)

def main():
    with open("../tests/disasm", "r") as fp:
        disasm = fp.read()
        assemble(disasm, "test")
if __name__ == '__main__':
    main()
