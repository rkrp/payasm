#!/usr/bin/python2

import opcode
from types import CodeType
import struct
import marshal
import ast

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
                self.arg_val = ast.literal_eval(' '.join(inst[2:]))
            except KeyError:
                pass

    def __repr__(self):
        return self.raw


WHITESPACE_LEN = 16

def get_constants(inst):
    if inst.opcode != "LOAD_CONST":
        raise Exception("Cannot load constant value for " + inst.opcode)
    return (inst.arg, inst.arg_val)


def populate_args(inst):
    if inst.has_arg:
        return struct.pack('H', inst.arg)
    else:
        return ''

def assemble(disasm, target_name):
    code = ''
    insts = [inst[WHITESPACE_LEN:] for inst in disasm.split('\n')]
    constants = {}
    for inst in insts:
        if inst.strip() == '':
            continue
        inst = Instruction(inst)

        #Generating bytecode
        code += chr(inst.opbyte)
        code += populate_args(inst)

        #Loading constants
        if inst.opcode == 'LOAD_CONST':
            (index, value) = get_constants(inst)
            constants[index] = value
            continue

    #populating constants tuple from the dict
    const_list = []
    try:
        i = 0
        while True:
            const_list.append(constants[i])
            i += 1
    except KeyError:
        pass
    const_list = tuple(const_list)

    filename = target_name + '.py'
    flags = 65
    firstlineno = 1
    lnotab = ''
    name = 'dummy'
    nlocals = 0
    names = ()
    varnames = ()
    code_type = CodeType(
            0,
            nlocals,
            100,
            flags,
            code,
            const_list,
            names,
            varnames,
            filename,
            name,
            firstlineno,
            lnotab
    )
    write_pyc(code_type, target_name + '.pyc')


def write_pyc(code, location):
    py_magic = '\x03\xf3\x0d\x0a'
    mod_time = '\xe9\xf5\x29\x59'
    code_str = marshal.dumps(code)
    pyc = py_magic + mod_time + code_str
    with open(location, 'w') as f:
        f.write(pyc)
