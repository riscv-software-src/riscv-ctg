# See LICENSE.incore for details

import os
from string import Template

root = os.path.abspath(os.path.dirname(__file__))

cwd = os.getcwd()
env = os.path.join(root,"env")

def sra(val, n):
    return val>>n if val >= 0 else (val+0x100000000) >> n
default_regset = ['x0' ,'x1' ,'x2' ,'x3' ,'x4' ,'x5' ,'x6' ,'x7' ,'x8' ,'x9'
            ,'x10' ,'x11' ,'x12' ,'x13' ,'x14' ,'x15' ,'x16' ,'x17' ,'x18' ,'x19'
            ,'x20' ,'x21' ,'x22' ,'x23' ,'x24' ,'x25' ,'x26' ,'x27' ,'x28' ,'x29'
            ,'x30' ,'x31']
default_regset_mx0 = ['x1' ,'x2' ,'x3' ,'x4' ,'x5' ,'x6' ,'x7' ,'x8' ,'x9'
            ,'x10' ,'x11' ,'x12' ,'x13' ,'x14' ,'x15' ,'x16' ,'x17' ,'x18' ,'x19'
            ,'x20' ,'x21' ,'x22' ,'x23' ,'x24' ,'x25' ,'x26' ,'x27' ,'x28' ,'x29'
            ,'x30' ,'x31']

def twos(val,bits):
    if isinstance(val,str):
        if '0x' in val:
            val = int(val,16)
        else:
            val = int(val,2)
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def gen_sign_dataset(bit_width):
    rval_w0_base = ['1']*(bit_width-1)+['0']
    rval_w1_base = ['0']*(bit_width-1)+['1']
    data = [(-2**(bit_width-1)),int((-2**(bit_width-1))/2),0,(2**(bit_width-1)-1),int((2**(bit_width-1)-1)/2)] + list(range(-10,10))
    data += [twos(''.join(rval_w1_base[n:] + rval_w1_base[:n]),bit_width) for n in range(bit_width)]
    data += [twos(''.join(rval_w0_base[n:] + rval_w0_base[:n]),bit_width) for n in range(bit_width)]
    t1 =( '' if bit_width%2 == 0 else '1') + ''.join(['01']*int(bit_width/2))
    t2 =( '' if bit_width%2 == 0 else '0') + ''.join(['10']*int(bit_width/2))
    data += [twos(t1,bit_width),twos(t2,bit_width)]
    return list(set(data))

def gen_usign_dataset(bit_width):
    rval_w0_base = ['1']*(bit_width-1)+['0']
    rval_w1_base = ['0']*(bit_width-1)+['1']
    data = [0,((2**bit_width)-1),int(((2**bit_width)-1)/2)] + list(range(0,20))
    data += [int(''.join(rval_w1_base[n:] + rval_w1_base[:n]),2) for n in range(bit_width)]
    data += [int(''.join(rval_w0_base[n:] + rval_w0_base[:n]),2) for n in range(bit_width)]
    t1 =( '' if bit_width%2 == 0 else '1') + ''.join(['01']*int(bit_width/2))
    t2 =( '' if bit_width%2 == 0 else '0') + ''.join(['10']*int(bit_width/2))
    data += [int(t1,2),int(t2,2)]
    return list(set(data))

template_file = os.path.join(root,"data/template.yaml")
copyright_string = ''''''
comment_template = '''
This assembly file tests the $opcode instruction of the RISC-V $extension extension for the $label covergroup.

'''
test_template = Template(copyright_string+comment_template+'''
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("$isa")

RVMODEL_BOOT
RVTEST_CODE_BEGIN
$test

RVMODEL_HALT
RVTEST_CODE_END

RVTEST_DATA_BEGIN
.align 4
$data
RVTEST_DATA_END

RVMODEL_DATA_BEGIN
$sig
RVMODEL_DATA_END
''')

case_template = Template('''
#ifdef TEST_CASE_$num
RVTEST_CASE($num,"//$cond;def TEST_CASE_$num=True;",$cov_label)
$code
#endif
''')

signode_template = Template('''
$label:
    .fill $n*(XLEN/32),4,0xafacadee
''')

