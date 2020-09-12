
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32I")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*);def TEST_CASE_1=True;",srli)
la x1,signature_x1_1
TEST_IMM_OP( srli, x31, x31, 1, -16777217, 31, x1, 0, x2)
TEST_IMM_OP( srli, x30, x29, 0, 1073741823, 31, x1, 4, x2)
TEST_IMM_OP( srli, x29, x30, 2130706431, -16777217, 0, x1, 8, x2)
TEST_IMM_OP( srli, x28, x27, 1073741823, 1073741823, 0, x1, 12, x2)
TEST_IMM_OP( srli, x27, x28, 0, 16, 16, x1, 16, x2)
TEST_IMM_OP( srli, x26, x25, 1, -2147483648, 31, x1, 20, x2)
TEST_IMM_OP( srli, x25, x26, 0, 0, 31, x1, 24, x2)
TEST_IMM_OP( srli, x24, x23, 0, 2147483647, 31, x1, 28, x2)
TEST_IMM_OP( srli, x23, x24, 0, 1, 31, x1, 32, x2)
TEST_IMM_OP( srli, x22, x21, 2139095039, -16777217, 1, x1, 36, x2)
TEST_IMM_OP( srli, x21, x22, 1069547519, -16777217, 2, x1, 40, x2)
TEST_IMM_OP( srli, x20, x19, 267386879, -16777217, 4, x1, 44, x2)
TEST_IMM_OP( srli, x19, x20, 16711679, -16777217, 8, x1, 48, x2)
TEST_IMM_OP( srli, x18, x17, 3, -16777217, 30, x1, 52, x2)
TEST_IMM_OP( srli, x17, x18, 7, -16777217, 29, x1, 56, x2)
TEST_IMM_OP( srli, x16, x15, 31, -16777217, 27, x1, 60, x2)
TEST_IMM_OP( srli, x15, x16, 509, -16777217, 23, x1, 64, x2)
TEST_IMM_OP( srli, x14, x13, 130559, -16777217, 15, x1, 68, x2)
TEST_IMM_OP( srli, x13, x14, 2039, -16777217, 21, x1, 72, x2)
TEST_IMM_OP( srli, x12, x11, 4177919, -16777217, 10, x1, 76, x2)
TEST_IMM_OP( srli, x11, x12, 0, 2, 31, x1, 80, x2)
TEST_IMM_OP( srli, x10, x9, 0, 4, 31, x1, 84, x2)
TEST_IMM_OP( srli, x9, x10, 0, 8, 31, x1, 88, x2)
TEST_IMM_OP( srli, x8, x7, 0, 32, 31, x1, 92, x2)
TEST_IMM_OP( srli, x7, x8, 0, 64, 31, x1, 96, x2)
TEST_IMM_OP( srli, x6, x5, 0, 128, 31, x1, 100, x2)
TEST_IMM_OP( srli, x5, x6, 0, 256, 31, x1, 104, x7)
TEST_IMM_OP( srli, x4, x3, 0, 512, 31, x1, 108, x7)
la x5,signature_x5_0
TEST_IMM_OP( srli, x3, x4, 0, 1024, 31, x5, 0, x7)
TEST_IMM_OP( srli, x2, x1, 0, 2048, 31, x5, 4, x7)
TEST_IMM_OP( srli, x1, x2, 0, 4096, 31, x5, 8, x7)
TEST_IMM_OP( srli, x31, x0, 0, 8192, 31, x5, 12, x7)
TEST_IMM_OP( srli, x0, x31, 0, 16384, 31, x5, 16, x7)
TEST_IMM_OP( srli, x11, x10, 0, 32768, 31, x5, 20, x7)
TEST_IMM_OP( srli, x11, x10, 0, 65536, 31, x5, 24, x7)
TEST_IMM_OP( srli, x11, x10, 0, 131072, 31, x5, 28, x7)
TEST_IMM_OP( srli, x11, x10, 0, 262144, 31, x5, 32, x7)
TEST_IMM_OP( srli, x11, x10, 0, 524288, 31, x5, 36, x7)
TEST_IMM_OP( srli, x11, x10, 0, 1048576, 31, x5, 40, x7)
TEST_IMM_OP( srli, x11, x10, 0, 2097152, 31, x5, 44, x7)
TEST_IMM_OP( srli, x11, x10, 0, 4194304, 31, x5, 48, x7)
TEST_IMM_OP( srli, x11, x10, 0, 8388608, 31, x5, 52, x7)
TEST_IMM_OP( srli, x11, x10, 0, 16777216, 31, x5, 56, x7)
TEST_IMM_OP( srli, x11, x10, 0, 33554432, 31, x5, 60, x7)
TEST_IMM_OP( srli, x11, x10, 0, 67108864, 31, x5, 64, x7)
TEST_IMM_OP( srli, x11, x10, 0, 134217728, 31, x5, 68, x7)
TEST_IMM_OP( srli, x11, x10, 0, 268435456, 31, x5, 72, x7)
TEST_IMM_OP( srli, x11, x10, 0, 536870912, 31, x5, 76, x7)
TEST_IMM_OP( srli, x11, x10, 0, 1073741824, 31, x5, 80, x7)
TEST_IMM_OP( srli, x11, x10, 1, -2, 31, x5, 84, x7)
TEST_IMM_OP( srli, x11, x10, 1, -513, 31, x5, 88, x7)
TEST_IMM_OP( srli, x11, x10, 1, -1025, 31, x5, 92, x7)
TEST_IMM_OP( srli, x11, x10, 1, -2049, 31, x5, 96, x7)
TEST_IMM_OP( srli, x11, x10, 1, -4097, 31, x5, 100, x7)
TEST_IMM_OP( srli, x11, x10, 1, -8193, 31, x5, 104, x7)
TEST_IMM_OP( srli, x11, x10, 1, -16385, 31, x5, 108, x7)
TEST_IMM_OP( srli, x11, x10, 1, -32769, 31, x5, 112, x7)
TEST_IMM_OP( srli, x11, x10, 1, -65537, 31, x5, 116, x7)
TEST_IMM_OP( srli, x11, x10, 1, -131073, 31, x5, 120, x7)
TEST_IMM_OP( srli, x11, x10, 1, -262145, 31, x5, 124, x7)
TEST_IMM_OP( srli, x11, x10, 1, -524289, 31, x5, 128, x7)
TEST_IMM_OP( srli, x11, x10, 1, -1048577, 31, x5, 132, x7)
TEST_IMM_OP( srli, x11, x10, 1, -2097153, 31, x5, 136, x7)
TEST_IMM_OP( srli, x11, x10, 1, -4194305, 31, x5, 140, x7)
TEST_IMM_OP( srli, x11, x10, 1, -8388609, 31, x5, 144, x7)
TEST_IMM_OP( srli, x11, x10, 1, -33554433, 31, x5, 148, x7)
TEST_IMM_OP( srli, x11, x10, 1, -9, 31, x5, 152, x7)
TEST_IMM_OP( srli, x11, x10, 1, -67108865, 31, x5, 156, x7)
TEST_IMM_OP( srli, x11, x10, 1, -134217729, 31, x5, 160, x7)
TEST_IMM_OP( srli, x11, x10, 1, -268435457, 31, x5, 164, x7)
TEST_IMM_OP( srli, x11, x10, 1, -536870913, 31, x5, 168, x7)
TEST_IMM_OP( srli, x11, x10, 1, -1073741825, 31, x5, 172, x7)
TEST_IMM_OP( srli, x11, x10, 0, 1431655765, 31, x5, 176, x7)
TEST_IMM_OP( srli, x11, x10, 1, -1431655766, 31, x5, 180, x7)
TEST_IMM_OP( srli, x11, x10, 1, -3, 31, x5, 184, x7)
TEST_IMM_OP( srli, x11, x10, 1, -5, 31, x5, 188, x7)
TEST_IMM_OP( srli, x11, x10, 1, -17, 31, x5, 192, x7)
TEST_IMM_OP( srli, x11, x10, 1, -33, 31, x5, 196, x7)
TEST_IMM_OP( srli, x11, x10, 1, -65, 31, x5, 200, x7)
TEST_IMM_OP( srli, x11, x10, 1, -129, 31, x5, 204, x7)
TEST_IMM_OP( srli, x11, x10, 1, -257, 31, x5, 208, x7)
TEST_IMM_OP( srli, x11, x10, 1, -16777217, 31, x5, 212, x7)
TEST_IMM_OP( srli, x11, x10, 0, 8192, 31, x5, 216, x7)
TEST_IMM_OP( srli, x11, x10, 0, 16384, 31, x5, 220, x7)
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
    .fill 56*(XLEN/32),4,0xafacadee

RVMODEL_DATA_END
