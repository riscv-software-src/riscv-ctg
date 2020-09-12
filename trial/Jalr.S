
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32I")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*);def TEST_CASE_1=True;",jalr)
la x1,signature_x1_1
TEST_JALR_OP(x2, x31, x31, 2047, x1, 0)
TEST_JALR_OP(x2, x29, x30, -1, x1, 4)
TEST_JALR_OP(x2, x30, x29, 1, x1, 8)
TEST_JALR_OP(x2, x27, x28, 2, x1, 12)
TEST_JALR_OP(x2, x28, x27, 4, x1, 16)
TEST_JALR_OP(x2, x25, x26, 8, x1, 20)
TEST_JALR_OP(x2, x26, x25, 16, x1, 24)
TEST_JALR_OP(x2, x23, x24, 32, x1, 28)
TEST_JALR_OP(x2, x24, x23, 64, x1, 32)
TEST_JALR_OP(x2, x21, x22, 128, x1, 36)
TEST_JALR_OP(x2, x22, x21, 256, x1, 40)
TEST_JALR_OP(x2, x19, x20, 512, x1, 44)
TEST_JALR_OP(x2, x20, x19, 1024, x1, 48)
TEST_JALR_OP(x2, x17, x18, -2048, x1, 52)
TEST_JALR_OP(x2, x18, x17, -2, x1, 56)
TEST_JALR_OP(x2, x15, x16, -3, x1, 60)
TEST_JALR_OP(x2, x16, x15, -5, x1, 64)
TEST_JALR_OP(x2, x13, x14, -9, x1, 68)
TEST_JALR_OP(x2, x14, x13, -17, x1, 72)
TEST_JALR_OP(x2, x11, x12, -33, x1, 76)
TEST_JALR_OP(x2, x12, x11, -65, x1, 80)
TEST_JALR_OP(x2, x9, x10, -129, x1, 84)
TEST_JALR_OP(x2, x10, x9, -257, x1, 88)
TEST_JALR_OP(x2, x7, x8, -1025, x1, 92)
TEST_JALR_OP(x2, x8, x7, 1365, x1, 96)
TEST_JALR_OP(x2, x5, x6, -1366, x1, 100)
TEST_JALR_OP(x7, x6, x5, -513, x1, 104)
TEST_JALR_OP(x7, x3, x4, -2048, x1, 108)
la x5,signature_x5_0
TEST_JALR_OP(x7, x4, x3, -2048, x5, 0)
TEST_JALR_OP(x7, x1, x2, -2048, x5, 4)
TEST_JALR_OP(x7, x2, x1, -2048, x5, 8)
TEST_JALR_OP(x7, x0, x31, -2048, x5, 12)
TEST_JALR_OP(x7, x11, x10, 2047, x5, 16)
TEST_JALR_OP(x7, x11, x10, -2048, x5, 20)
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
