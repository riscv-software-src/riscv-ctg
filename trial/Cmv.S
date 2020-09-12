
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32IC")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*C.*);def TEST_CASE_1=True;",cmv)
la x1,signature_x1_1
TEST_CMV_OP( c.mv, x30, x31, 0, -2147483648, x1, 0, x2)
TEST_CMV_OP( c.mv, x29, x29, 0, 0, x1, 4, x2)
TEST_CMV_OP( c.mv, x31, x30, 0, 2147483647, x1, 8, x2)
TEST_CMV_OP( c.mv, x27, x28, 0, 1, x1, 12, x2)
TEST_CMV_OP( c.mv, x28, x27, 0, 2, x1, 16, x2)
TEST_CMV_OP( c.mv, x25, x26, 0, 4, x1, 20, x2)
TEST_CMV_OP( c.mv, x26, x25, 0, 8, x1, 24, x2)
TEST_CMV_OP( c.mv, x23, x24, 0, 16, x1, 28, x2)
TEST_CMV_OP( c.mv, x24, x23, 0, 32, x1, 32, x2)
TEST_CMV_OP( c.mv, x21, x22, 0, 64, x1, 36, x2)
TEST_CMV_OP( c.mv, x22, x21, 0, 128, x1, 40, x2)
TEST_CMV_OP( c.mv, x19, x20, 0, 256, x1, 44, x2)
TEST_CMV_OP( c.mv, x20, x19, 0, 512, x1, 48, x2)
TEST_CMV_OP( c.mv, x17, x18, 0, 1024, x1, 52, x2)
TEST_CMV_OP( c.mv, x18, x17, 0, 2048, x1, 56, x2)
TEST_CMV_OP( c.mv, x15, x16, 0, 4096, x1, 60, x2)
TEST_CMV_OP( c.mv, x16, x15, 0, 8192, x1, 64, x2)
TEST_CMV_OP( c.mv, x13, x14, 0, 16384, x1, 68, x2)
TEST_CMV_OP( c.mv, x14, x13, 0, 32768, x1, 72, x2)
TEST_CMV_OP( c.mv, x11, x12, 0, 65536, x1, 76, x2)
TEST_CMV_OP( c.mv, x12, x11, 0, 131072, x1, 80, x2)
TEST_CMV_OP( c.mv, x9, x10, 0, 262144, x1, 84, x2)
TEST_CMV_OP( c.mv, x10, x9, 0, 524288, x1, 88, x2)
TEST_CMV_OP( c.mv, x7, x8, 0, 1048576, x1, 92, x2)
TEST_CMV_OP( c.mv, x8, x7, 0, 2097152, x1, 96, x2)
TEST_CMV_OP( c.mv, x5, x6, 0, 4194304, x1, 100, x2)
TEST_CMV_OP( c.mv, x6, x5, 0, 8388608, x1, 104, x7)
TEST_CMV_OP( c.mv, x3, x4, 0, 16777216, x1, 108, x7)
la x5,signature_x5_0
TEST_CMV_OP( c.mv, x4, x3, 0, 33554432, x5, 0, x7)
TEST_CMV_OP( c.mv, x1, x2, 0, 67108864, x5, 4, x7)
TEST_CMV_OP( c.mv, x2, x1, 0, 134217728, x5, 8, x7)
TEST_CMV_OP( c.mv, x0, x31, 0, 268435456, x5, 12, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, 536870912, x5, 16, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, 1073741824, x5, 20, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -2, x5, 24, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -3, x5, 28, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -536870913, x5, 32, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -1073741825, x5, 36, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, 1431655765, x5, 40, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -1431655766, x5, 44, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -5, x5, 48, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -9, x5, 52, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -17, x5, 56, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -33, x5, 60, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -65, x5, 64, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -129, x5, 68, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -257, x5, 72, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -513, x5, 76, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -1025, x5, 80, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -2049, x5, 84, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -4097, x5, 88, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -8193, x5, 92, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -16385, x5, 96, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -32769, x5, 100, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -65537, x5, 104, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -131073, x5, 108, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -262145, x5, 112, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -524289, x5, 116, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -1048577, x5, 120, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -2097153, x5, 124, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -4194305, x5, 128, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -8388609, x5, 132, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -16777217, x5, 136, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -33554433, x5, 140, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -67108865, x5, 144, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -134217729, x5, 148, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, -268435457, x5, 152, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, 0, x5, 156, x7)
TEST_CMV_OP( c.mv, x10, x11, 0, 268435456, x5, 160, x7)
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
    .fill 41*(XLEN/32),4,0xafacadee

RVMODEL_DATA_END
