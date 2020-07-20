# See LICENSE.incore for details

import os
from string import Template

root = os.path.abspath(os.path.dirname(__file__))

cwd = os.getcwd()
env = os.path.join(root,"env")
default_regset = ['x0' ,'x1' ,'x2' ,'x3' ,'x4' ,'x5' ,'x6' ,'x7' ,'x8' ,'x9'
        ,'x10' ,'x11' ,'x12' ,'x13' ,'x14' ,'x15' ,'x16' ,'x17' ,'x18' ,'x19'
        ,'x20' ,'x21' ,'x22' ,'x23' ,'x24' ,'x25' ,'x26' ,'x27' ,'x28' ,'x29'
        ,'x30' ,'x31']
default_regset_mx0 = ['x1' ,'x2' ,'x3' ,'x4' ,'x5' ,'x6' ,'x7' ,'x8' ,'x9'
        ,'x10' ,'x11' ,'x12' ,'x13' ,'x14' ,'x15' ,'x16' ,'x17' ,'x18' ,'x19'
        ,'x20' ,'x21' ,'x22' ,'x23' ,'x24' ,'x25' ,'x26' ,'x27' ,'x28' ,'x29'
        ,'x30' ,'x31']
def sra(val, n):
    return val>>n if val >= 0 else (val+0x100000000) >> n
imm_min = -2**12
imm_max = 2**12
shift_min = 0
shift_max = 31
xlen = 32
int32_min = -50
int32_max = 50
template_file = os.path.join(root,"data/template.yaml")

test_template = Template('''
# For Licence details look at https://gitlab.com/incoresemi/riscv-compliance/riscv_ctg/-/blob/master/LICENSE.incore
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
    .fill $n,4,0xafacadee
''')

