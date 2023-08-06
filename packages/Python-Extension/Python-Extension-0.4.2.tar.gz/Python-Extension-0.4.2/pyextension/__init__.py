import platform as p
import sys

class computer:
    name = p.node()
    os = p.system()
    processor = p.processor()
    machine = p.machine()
    release = p.release()
    platform = p.platform()
    version = p.version()

def computer():
    PC = ''
    PC += '===== %s =====' % p.node()
    PC += '\n'
    PC += '''OS:
    %s''' % p.system()
    PC += '\n'
    PC += '''Processor:
    %s''' % p.processor()
    PC += '\n'
    PC += '''Machine:
    %s''' % p.machine()
    PC += '\n'
    PC += '''Release:
    %s''' % p.release()
    PC += '\n'
    PC += '''Platform:
    %s''' % p.platform()
    PC += '\n'
    PC += '''Version:
    %s''' % p.version()
    return PC

class python:
    ver = str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2])
    version = sys.version
    build = p.python_build()

def python():
    PYTHON = ''
    PYTHON += '===== Python ' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2]) + ' ====='
    PYTHON += '\n'
    PYTHON += 'Version : '
    PYTHON += '\n'
    PYTHON += 4 * ' '
    PYTHON += sys.version
    PYTHON += '\n'
    PYTHON += 'Build : '
    PYTHON += '\n'
    PYTHON += 4 * ' '
    PYTHON += str(p.python_build())
    return PYTHON
