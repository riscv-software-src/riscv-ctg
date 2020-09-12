
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32I")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*);def TEST_CASE_1=True;",slti)
la x1,signature_x1_1
TEST_IMM_OP( slti, x31, x31, 0, -1, -1, x1, 0, x2)
TEST_IMM_OP( slti, x30, x29, 1, -16777217, 2047, x1, 4, x2)
TEST_IMM_OP( slti, x29, x30, 0, 1073741823, 2047, x1, 8, x2)
TEST_IMM_OP( slti, x28, x27, 0, 1073741823, -1, x1, 12, x2)
TEST_IMM_OP( slti, x27, x28, 1, -2147483648, 2047, x1, 16, x2)
TEST_IMM_OP( slti, x26, x25, 1, 0, 2047, x1, 20, x2)
TEST_IMM_OP( slti, x25, x26, 0, 2147483647, 2047, x1, 24, x2)
TEST_IMM_OP( slti, x24, x23, 1, 1, 2047, x1, 28, x2)
TEST_IMM_OP( slti, x23, x24, 1, -16777217, -2048, x1, 32, x2)
TEST_IMM_OP( slti, x22, x21, 1, -16777217, 0, x1, 36, x2)
TEST_IMM_OP( slti, x21, x22, 1, -16777217, 1, x1, 40, x2)
TEST_IMM_OP( slti, x20, x19, 1, 2, 2047, x1, 44, x2)
TEST_IMM_OP( slti, x19, x20, 1, 4, 2047, x1, 48, x2)
TEST_IMM_OP( slti, x18, x17, 1, 8, 2047, x1, 52, x2)
TEST_IMM_OP( slti, x17, x18, 1, 16, 2047, x1, 56, x2)
TEST_IMM_OP( slti, x16, x15, 1, 32, 2047, x1, 60, x2)
TEST_IMM_OP( slti, x15, x16, 1, 64, 2047, x1, 64, x2)
TEST_IMM_OP( slti, x14, x13, 1, 128, 2047, x1, 68, x2)
TEST_IMM_OP( slti, x13, x14, 1, 256, 2047, x1, 72, x2)
TEST_IMM_OP( slti, x12, x11, 1, 512, 2047, x1, 76, x2)
TEST_IMM_OP( slti, x11, x12, 1, 1024, 2047, x1, 80, x2)
TEST_IMM_OP( slti, x10, x9, 0, 2048, 2047, x1, 84, x2)
TEST_IMM_OP( slti, x9, x10, 0, 4096, 2047, x1, 88, x2)
TEST_IMM_OP( slti, x8, x7, 0, 8192, 2047, x1, 92, x2)
TEST_IMM_OP( slti, x7, x8, 0, 16384, 2047, x1, 96, x2)
TEST_IMM_OP( slti, x6, x5, 0, 32768, 2047, x1, 100, x2)
TEST_IMM_OP( slti, x5, x6, 0, 65536, 2047, x1, 104, x7)
TEST_IMM_OP( slti, x4, x3, 0, 131072, 2047, x1, 108, x7)
la x5,signature_x5_0
TEST_IMM_OP( slti, x3, x4, 0, 262144, 2047, x5, 0, x7)
TEST_IMM_OP( slti, x2, x1, 0, 524288, 2047, x5, 4, x7)
TEST_IMM_OP( slti, x1, x2, 0, 1048576, 2047, x5, 8, x7)
TEST_IMM_OP( slti, x31, x0, 0, 2097152, 2047, x5, 12, x7)
TEST_IMM_OP( slti, x0, x31, 0, 4194304, 2047, x5, 16, x7)
TEST_IMM_OP( slti, x11, x10, 0, 8388608, 2047, x5, 20, x7)
TEST_IMM_OP( slti, x11, x10, 0, 16777216, 2047, x5, 24, x7)
TEST_IMM_OP( slti, x11, x10, 0, 33554432, 2047, x5, 28, x7)
TEST_IMM_OP( slti, x11, x10, 0, 67108864, 2047, x5, 32, x7)
TEST_IMM_OP( slti, x11, x10, 0, 134217728, 2047, x5, 36, x7)
TEST_IMM_OP( slti, x11, x10, 0, 268435456, 2047, x5, 40, x7)
TEST_IMM_OP( slti, x11, x10, 0, 536870912, 2047, x5, 44, x7)
TEST_IMM_OP( slti, x11, x10, 0, 1073741824, 2047, x5, 48, x7)
TEST_IMM_OP( slti, x11, x10, 1, -2, 2047, x5, 52, x7)
TEST_IMM_OP( slti, x11, x10, 1, -3, 2047, x5, 56, x7)
TEST_IMM_OP( slti, x11, x10, 1, -5, 2047, x5, 60, x7)
TEST_IMM_OP( slti, x11, x10, 1, -9, 2047, x5, 64, x7)
TEST_IMM_OP( slti, x11, x10, 1, -17, 2047, x5, 68, x7)
TEST_IMM_OP( slti, x11, x10, 1, -33, 2047, x5, 72, x7)
TEST_IMM_OP( slti, x11, x10, 1, -65, 2047, x5, 76, x7)
TEST_IMM_OP( slti, x11, x10, 1, -129, 2047, x5, 80, x7)
TEST_IMM_OP( slti, x11, x10, 1, -257, 2047, x5, 84, x7)
TEST_IMM_OP( slti, x11, x10, 1, -513, 2047, x5, 88, x7)
TEST_IMM_OP( slti, x11, x10, 1, -1025, 2047, x5, 92, x7)
TEST_IMM_OP( slti, x11, x10, 1, -2049, 2047, x5, 96, x7)
TEST_IMM_OP( slti, x11, x10, 1, -4097, 2047, x5, 100, x7)
TEST_IMM_OP( slti, x11, x10, 1, -8193, 2047, x5, 104, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16385, 2047, x5, 108, x7)
TEST_IMM_OP( slti, x11, x10, 1, -32769, 2047, x5, 112, x7)
TEST_IMM_OP( slti, x11, x10, 1, -65537, 2047, x5, 116, x7)
TEST_IMM_OP( slti, x11, x10, 1, -131073, 2047, x5, 120, x7)
TEST_IMM_OP( slti, x11, x10, 1, -262145, 2047, x5, 124, x7)
TEST_IMM_OP( slti, x11, x10, 1, -524289, 2047, x5, 128, x7)
TEST_IMM_OP( slti, x11, x10, 1, -1048577, 2047, x5, 132, x7)
TEST_IMM_OP( slti, x11, x10, 1, -2097153, 2047, x5, 136, x7)
TEST_IMM_OP( slti, x11, x10, 1, -4194305, 2047, x5, 140, x7)
TEST_IMM_OP( slti, x11, x10, 1, -8388609, 2047, x5, 144, x7)
TEST_IMM_OP( slti, x11, x10, 1, -33554433, 2047, x5, 148, x7)
TEST_IMM_OP( slti, x11, x10, 1, -67108865, 2047, x5, 152, x7)
TEST_IMM_OP( slti, x11, x10, 1, -134217729, 2047, x5, 156, x7)
TEST_IMM_OP( slti, x11, x10, 1, -268435457, 2047, x5, 160, x7)
TEST_IMM_OP( slti, x11, x10, 1, -536870913, 2047, x5, 164, x7)
TEST_IMM_OP( slti, x11, x10, 1, -1073741825, 2047, x5, 168, x7)
TEST_IMM_OP( slti, x11, x10, 0, 1431655765, 2047, x5, 172, x7)
TEST_IMM_OP( slti, x11, x10, 1, -1431655766, 2047, x5, 176, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 2, x5, 180, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 4, x5, 184, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 8, x5, 188, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 16, x5, 192, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 32, x5, 196, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 64, x5, 200, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 128, x5, 204, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 256, x5, 208, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -65, x5, 212, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -129, x5, 216, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -257, x5, 220, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -513, x5, 224, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -1025, x5, 228, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 1365, x5, 232, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -1366, x5, 236, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 512, x5, 240, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, 1024, x5, 244, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -2, x5, 248, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -3, x5, 252, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -5, x5, 256, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -9, x5, 260, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -17, x5, 264, x7)
TEST_IMM_OP( slti, x11, x10, 1, -16777217, -33, x5, 268, x7)
TEST_IMM_OP( slti, x11, x10, 0, -1, -1, x5, 272, x7)
TEST_IMM_OP( slti, x11, x10, 0, 2097152, 2047, x5, 276, x7)
TEST_IMM_OP( slti, x11, x10, 0, 4194304, 2047, x5, 280, x7)
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
    .fill 71*(XLEN/32),4,0xafacadee

RVMODEL_DATA_END
