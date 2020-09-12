
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32I")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*);def TEST_CASE_1=True;",lbu-align)
la x1,signature_x1_1
TEST_LOAD(x1,x2,0,x31,x31,-4,0,lbu,0)
TEST_LOAD(x1,x2,0,x30,x29,-3,4,lbu,0)
TEST_LOAD(x1,x2,0,x29,x30,-6,8,lbu,0)
TEST_LOAD(x1,x2,0,x28,x27,2047,12,lbu,0)
TEST_LOAD(x1,x2,0,x27,x28,-4,16,lbu,2)
TEST_LOAD(x1,x2,0,x26,x25,-3,20,lbu,2)
TEST_LOAD(x1,x2,0,x25,x26,-6,24,lbu,2)
TEST_LOAD(x1,x2,0,x24,x23,2047,28,lbu,2)
TEST_LOAD(x1,x2,0,x23,x24,-4,32,lbu,1)
TEST_LOAD(x1,x2,0,x22,x21,-3,36,lbu,1)
TEST_LOAD(x1,x2,0,x21,x22,0,40,lbu,0)
TEST_LOAD(x1,x2,0,x20,x19,-6,44,lbu,1)
TEST_LOAD(x1,x2,0,x19,x20,2047,48,lbu,1)
TEST_LOAD(x1,x2,0,x18,x17,-4,52,lbu,3)
TEST_LOAD(x1,x2,0,x17,x18,-3,56,lbu,3)
TEST_LOAD(x1,x2,0,x16,x15,-6,60,lbu,3)
TEST_LOAD(x1,x2,0,x15,x16,2047,64,lbu,3)
TEST_LOAD(x1,x2,0,x14,x13,-2048,68,lbu,0)
TEST_LOAD(x1,x2,0,x13,x14,-2048,72,lbu,0)
TEST_LOAD(x1,x2,0,x12,x11,-2048,76,lbu,0)
TEST_LOAD(x1,x2,0,x11,x12,-2048,80,lbu,0)
TEST_LOAD(x1,x2,0,x10,x9,-2048,84,lbu,0)
TEST_LOAD(x1,x2,0,x9,x10,-2048,88,lbu,0)
TEST_LOAD(x1,x2,0,x8,x7,-2048,92,lbu,0)
TEST_LOAD(x1,x2,0,x7,x8,-2048,96,lbu,0)
TEST_LOAD(x1,x2,0,x6,x5,-2048,100,lbu,0)
TEST_LOAD(x1,x7,0,x5,x6,-2048,104,lbu,0)
TEST_LOAD(x1,x7,0,x4,x3,-2048,108,lbu,0)
la x5,signature_x5_0
TEST_LOAD(x5,x7,0,x3,x4,-2048,0,lbu,0)
TEST_LOAD(x5,x7,0,x2,x1,-2048,4,lbu,0)
TEST_LOAD(x5,x7,0,x1,x2,-2048,8,lbu,0)
TEST_LOAD(x5,x7,0,x31,x0,-2048,12,lbu,0)
TEST_LOAD(x5,x7,0,x10,x11,-4,16,lbu,0)
TEST_LOAD(x5,x7,0,x10,x11,-2048,20,lbu,0)
#endif


RVMODEL_HALT
RVTEST_CODE_END

RVTEST_DATA_BEGIN
.align 4
.align 4
rvtest_data:
.word 0xbabecafe
RVTEST_DATA_END

RVMODEL_DATA_BEGIN
.align 4

signature_x1_0:
    .fill 0*(XLEN/32),4,0xafacadee


signature_x1_1:
    .fill 28*(XLEN/32),4,0xafacadee


signature_x5_0:
    .fill 6*(XLEN/32),4,0xafacadee

RVMODEL_DATA_END
