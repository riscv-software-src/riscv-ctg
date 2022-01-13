# See LICENSE.incore for details

import os
from math import *
from string import Template
from riscv_isac.fp_dataset import *

root = os.path.abspath(os.path.dirname(__file__))

cwd = os.getcwd()
env = os.path.join(root,"env")

default_regset = ['x0' ,'x1' ,'x2' ,'x3' ,'x4' ,'x5' ,'x6' ,'x7' ,'x8' ,'x9'
            ,'x10' ,'x11' ,'x12' ,'x13' ,'x14' ,'x15' ,'x16' ,'x17' ,'x18' ,'x19'
            ,'x20' ,'x21' ,'x22' ,'x23' ,'x24' ,'x25' ,'x26' ,'x27' ,'x28' ,'x29'
            ,'x30' ,'x31']
default_fregset = ['f0' ,'f1' ,'f2' ,'f3' ,'f4' ,'f5' ,'f6' ,'f7' ,'f8' ,'f9'
            ,'f10' ,'f11' ,'f12' ,'f13' ,'f14' ,'f15' ,'f16' ,'f17' ,'f18' ,'f19'
            ,'f20' ,'f21' ,'f22' ,'f23' ,'f24' ,'f25' ,'f26' ,'f27' ,'f28' ,'f29'
            ,'f30' ,'f31']
e_regset = ['x0' ,'x1' ,'x2' ,'x3' ,'x4' ,'x5' ,'x6' ,'x7' ,'x8' ,'x9'
            ,'x10' ,'x11' ,'x12' ,'x13' ,'x14' ,'x15']
default_regset_mx0 = ['x1' ,'x2' ,'x3' ,'x4' ,'x5' ,'x6' ,'x7' ,'x8' ,'x9'
            ,'x10' ,'x11' ,'x12' ,'x13' ,'x14' ,'x15' ,'x16' ,'x17' ,'x18' ,'x19'
            ,'x20' ,'x21' ,'x22' ,'x23' ,'x24' ,'x25' ,'x26' ,'x27' ,'x28' ,'x29'
            ,'x30' ,'x31']

def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def twos(val,bits):
    '''
    A function to generate the two's complement of a number which is of
    arbitrary width

    :param val: the input which can be either a hexadecimal string or integer
    :param bits: size of the input in terms of bits.

    :type val: Union[int, str]
    :type bits: int

    :return: integer value in 2's complement representation
    '''
    if isinstance(val,str):
        if '0x' in val:
            val = int(val,16)
        else:
            val = int(val,2)
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def gen_imm_dataset(bit_width):
    '''
    Function to enumerate a dataset for immediate values:
     - [0,2**bit_width]

     :param bit_width: Integer defining the size of the input
     :type bit_width: int
     :return: a list of integers
    '''
    usign_val = (2**(bit_width))
    dataset = []
    for i in range(usign_val):
        dataset.append(i)
    return dataset

def gen_sp_dataset(bit_width,sign=True):
    '''
    Function generates a special dataset of interesting values:
     - [3*1/3,3*2/3,5,5*1/5,5*2/5]
     - sqrt (bit_width<<1)
     - +/-1 variants of the above

     :param bit_width: Integer defining the size of the input
     :param sign: Boolen value specifying whether the dataset should be interpreted as signed numbers or not.
     :type sign: bool
     :type bit_width: int
     :return: a list of integers
    '''
    if sign:
        conv_func = lambda x: twos(x,bit_width)
        sqrt_min = int(-sqrt(2**(bit_width-1)))
        sqrt_max = int(sqrt((2**(bit_width-1)-1)))
    else:
        sqrt_min = 0
        sqrt_max = int(sqrt((2**bit_width)-1))
        conv_func = lambda x:(int(x,16) if '0x' in x else int(x,2)) if isinstance(x,str) else x

    dataset = [3, "0x"+"".join(["5"]*int(bit_width/4)), "0x"+"".join(["a"]*int(bit_width/4)), 5, "0x"+"".join(["3"]*int(bit_width/4)), "0x"+"".join(["6"]*int(bit_width/4))]
    dataset = list(map(conv_func,dataset)) + [int(sqrt(abs(conv_func("0x8"+"".join(["0"]*int((bit_width/4)-1)))))*(-1 if sign else 1))] + [sqrt_min,sqrt_max]
    return dataset + [x - 1 if x > 0 else 0 for x in dataset] + [x+1 for x in dataset]

# def gen_fp_dataset(flen,instr,field):
#         return (ibm_dataset(flen,instr,field))   # Dataset will be returned by isac

def gen_sign_dataset(bit_width):
    '''
    Function to generate the signed data set with datapoints from the following patterns.
     - alternating ones
     - alternating zeros
     - walking ones
     - walking zeros
     - max val
     - min val
     - max val/2
     - min val/2
     - [-10,10]

     :param bit_width: integer defining the size of the input
     :type bit_width: int
     :return: a list of integers
    '''
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
    '''
    Function to generate the unsigned dataset
     - alternating ones
     - alternating zeros
     - walking ones
     - walking zeros
     - max val
     - min val
     - max val/2
     - min val/2
     - [0,20]

     :param bit_width: integer defining the size of the input
     :type bit_width: int
     :return: a list of integers
    '''
    rval_w0_base = ['1']*(bit_width-1)+['0']
    rval_w1_base = ['0']*(bit_width-1)+['1']
    data = [0,((2**bit_width)-1),int(((2**bit_width)-1)/2)] + list(range(0,20))
    data += [int(''.join(rval_w1_base[n:] + rval_w1_base[:n]),2) for n in range(bit_width)]
    data += [int(''.join(rval_w0_base[n:] + rval_w0_base[:n]),2) for n in range(bit_width)]
    t1 =( '' if bit_width%2 == 0 else '1') + ''.join(['01']*int(bit_width/2))
    t2 =( '' if bit_width%2 == 0 else '0') + ''.join(['10']*int(bit_width/2))
    data += [int(t1,2),int(t2,2)]
    return list(set(data))

def zerotoxlen(bit_width):
    vals = []
    for i in range(bit_width):
        vals.append(i)
    return vals


template_file = os.path.join(root,"data/template.yaml")

usage = Template('''
// -----------
// This file was generated by riscv_ctg (https://github.com/riscv-software-src/riscv-ctg)
// version   : $version
// timestamp : $time
// usage     : riscv_ctg \\
//                  -- cgf $cgf \\
//                  -- xlen $xlen $randomize \\
// -----------
//''')

copyright_string = '''
// -----------
// Copyright (c) 2020. RISC-V International. All rights reserved.
// SPDX-License-Identifier: BSD-3-Clause
// -----------
//'''

comment_template = '''
// This assembly file tests the $opcode instruction of the RISC-V $extension extension for the $label covergroup.
// '''

test_template = Template(copyright_string + comment_template+'''
#include "model_test.h"
#include "arch_test.h"
RVTEST_ISA("$isa")

.section .text.init
.globl rvtest_entry_point
rvtest_entry_point:
RVMODEL_BOOT
RVTEST_CODE_BEGIN
$test

RVTEST_CODE_END
RVMODEL_HALT

RVTEST_DATA_BEGIN
$data
RVTEST_DATA_END

RVMODEL_DATA_BEGIN
$sig
RVMODEL_DATA_END
''')
case_template = Template('''
RVTEST_CASE($num,"//check ISA:=regex(.*$xlen.*);$cond;def TEST_CASE_1=True;",$cov_label)
''')

part_template = Template('''
#ifdef TEST_CASE_1
$case_str
$code
#endif
''')

signode_template = Template('''
$label:
    .fill $n*(XLEN/32),4,0xdeadbeef
''')

