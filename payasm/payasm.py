#!/usr/bin/python2

import opcode
from types import CodeType
import struct
import marshal
import ast
import re

class Instruction:
    def __init__(self, inst, function):
        self.function = function
        self.raw = inst
        inst = inst.split()
        self.opcode = inst[0]
        self.opbyte = opcode.opmap[self.opcode]
        #Check if the instruction has arguments
        self.has_arg = self.opbyte >= 0x5a
        if self.has_arg:
            self.arg = int(inst[1])
            arg_val = ' '.join(inst[2:]).strip()
            try:
                if arg_val != '':
                    self.arg_val = ast.literal_eval(arg_val)
            #Handling names for LOAD_FAST and STORE_FAST
            #Both local variable identifiers and method names
            except ValueError:
                parts = re.findall("\((.*)\)", arg_val)
                if(len(parts) == 1):
                    self.arg_val = parts[0]
            #Handling comment-like args, like in SETUP_LOOP
            #where terminal instruction number is the arg_val
            except SyntaxError:
                pass

    def __repr__(self):
        return self.raw


WHITESPACE_LEN = 16

def get_constants(inst):
    if inst.opcode != "LOAD_CONST":
        raise Exception("Cannot load constant value for " + inst.opcode)
    return (inst.arg, inst.arg_val)

def get_identifier(inst):
    allowed = ['GLOBAL', 'FAST', 'ATTR']
    if filter(lambda x : x in inst.opcode, allowed) != 0:
        return (inst.arg, inst.arg_val)
    else:
        raise Exception("Cannot load name value for " + inst.opcode)

def populate_args(inst):
    if inst.has_arg:
        return struct.pack('H', inst.arg)
    else:
        return ''

def parse_instructions(disasm):
    insts = disasm.split('\n')
    fn_name = None
    instructions = []
    for inst in insts:
        if inst.strip() == '':
            continue

        #Check if a new function is starting
        fn_lt = re.findall("Disassembly of(.*):", inst)
        if len(fn_lt) == 1:
            fn_name = fn_lt[0]
            continue

        #Sanitize the whitespace and line number markers
        #TODO line number support for better stacktrace and decompilation
        inst = inst[WHITESPACE_LEN:]

        instructions.append(Instruction(inst, fn_name))
    return instructions


def assemble(instructions, target_name):
    constants = {}
    identifiers = {}
    global_names = {}

    code = ''
    for inst in instructions:
        #Generating bytecode
        code += chr(inst.opbyte)
        code += populate_args(inst)

        #Loading constants
        if inst.opcode == 'LOAD_CONST':
            (index, value) = get_constants(inst)
            constants[index] = value
            continue
        elif inst.opcode == 'STORE_FAST' or inst.opcode == 'LOAD_FAST':
            index, value = get_identifier(inst)
            identifiers[index] = value
        elif inst.opcode == 'LOAD_GLOBAL' or inst.opcode == 'LOAD_ATTR':
            index, value = get_identifier(inst)
            global_names[index] = value

    const_list = dict_to_tuple(constants)
    filename = target_name + '.py'
    flags = 65
    firstlineno = 1
    lnotab = ''
    name = 'dummy'
    nlocals = 0
    varnames = dict_to_tuple(identifiers)
    names = dict_to_tuple(global_names)

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
    return code_type

def dict_to_tuple(numdict):
    """populates constants from the dict with contigous
    integer keys from 0, to a tuple"""

    temp_list = []
    try:
        i = min(numdict)
        if i != 0:
            temp_list += [0] * i
        while True:
            temp_list.append(numdict[i])
            i += 1
    except KeyError:
        pass
    except ValueError:
        pass

    return tuple(temp_list)

def write_pyc(code, location):
    py_magic = '\x03\xf3\x0d\x0a'
    mod_time = '\xe9\xf5\x29\x59'
    code_str = marshal.dumps(code)
    pyc = py_magic + mod_time + code_str
    with open(location, 'w') as f:
        f.write(pyc)
