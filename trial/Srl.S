
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32i")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*);def TEST_CASE_1=True;",srl)
la x1,signature_x1_1
TEST_RR_OP(srl, x31, x30, x29, 1, -16777217, 31, x1, 0, x2)
TEST_RR_OP(srl, x29, x29, x31, 0, 1073741823, 31, x1, 4, x2)
TEST_RR_OP(srl, x30, x28, x28, 2130706431, -16777217, 0, x1, 8, x2)
TEST_RR_OP(srl, x27, x27, x27, 1073741823, 1073741823, 0, x1, 12, x2)
TEST_RR_OP(srl, x26, x31, x26, 0, 16, 16, x1, 16, x2)
TEST_RR_OP(srl, x28, x26, x30, 1, -2147483648, 31, x1, 20, x2)
TEST_RR_OP(srl, x25, x24, x23, 0, 0, 31, x1, 24, x2)
TEST_RR_OP(srl, x24, x23, x25, 0, 2147483647, 31, x1, 28, x2)
TEST_RR_OP(srl, x23, x25, x24, 0, 1, 31, x1, 32, x2)
TEST_RR_OP(srl, x22, x21, x20, 2139095039, -16777217, 1, x1, 36, x2)
TEST_RR_OP(srl, x21, x20, x22, 1069547519, -16777217, 2, x1, 40, x2)
TEST_RR_OP(srl, x20, x22, x21, 267386879, -16777217, 4, x1, 44, x2)
TEST_RR_OP(srl, x19, x18, x17, 16711679, -16777217, 8, x1, 48, x2)
TEST_RR_OP(srl, x18, x17, x19, 3, -16777217, 30, x1, 52, x2)
TEST_RR_OP(srl, x17, x19, x18, 7, -16777217, 29, x1, 56, x2)
TEST_RR_OP(srl, x16, x15, x14, 31, -16777217, 27, x1, 60, x2)
TEST_RR_OP(srl, x15, x14, x16, 509, -16777217, 23, x1, 64, x2)
TEST_RR_OP(srl, x14, x16, x15, 130559, -16777217, 15, x1, 68, x2)
TEST_RR_OP(srl, x13, x12, x11, 2039, -16777217, 21, x1, 72, x2)
TEST_RR_OP(srl, x12, x11, x13, 4177919, -16777217, 10, x1, 76, x2)
TEST_RR_OP(srl, x11, x13, x12, 0, 2, 31, x1, 80, x2)
TEST_RR_OP(srl, x10, x9, x8, 0, 4, 31, x1, 84, x2)
TEST_RR_OP(srl, x9, x8, x10, 0, 8, 31, x1, 88, x2)
TEST_RR_OP(srl, x8, x10, x9, 0, 32, 31, x1, 92, x2)
TEST_RR_OP(srl, x7, x6, x5, 0, 64, 31, x1, 96, x2)
TEST_RR_OP(srl, x6, x5, x7, 0, 128, 31, x1, 100, x8)
TEST_RR_OP(srl, x5, x7, x6, 0, 256, 31, x1, 104, x8)
TEST_RR_OP(srl, x4, x3, x2, 0, 512, 31, x1, 108, x8)
la x5,signature_x5_0
TEST_RR_OP(srl, x3, x2, x4, 0, 1024, 31, x5, 0, x8)
TEST_RR_OP(srl, x2, x4, x3, 0, 2048, 31, x5, 4, x8)
TEST_RR_OP(srl, x31, x1, x30, 0, 4096, 31, x5, 8, x8)
TEST_RR_OP(srl, x31, x0, x30, 0, 8192, 31, x5, 12, x8)
TEST_RR_OP(srl, x31, x30, x1, 0, 16384, 31, x5, 16, x8)
TEST_RR_OP(srl, x31, x30, x0, 0, 32768, 31, x5, 20, x8)
TEST_RR_OP(srl, x1, x31, x30, 0, 65536, 31, x5, 24, x8)
TEST_RR_OP(srl, x0, x31, x30, 0, 131072, 31, x5, 28, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 262144, 31, x5, 32, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 524288, 31, x5, 36, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 1048576, 31, x5, 40, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 2097152, 31, x5, 44, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 4194304, 31, x5, 48, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 8388608, 31, x5, 52, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 16777216, 31, x5, 56, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 33554432, 31, x5, 60, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 67108864, 31, x5, 64, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 134217728, 31, x5, 68, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 268435456, 31, x5, 72, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 536870912, 31, x5, 76, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 1073741824, 31, x5, 80, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -2, 31, x5, 84, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -2049, 31, x5, 88, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -4097, 31, x5, 92, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -8193, 31, x5, 96, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -16385, 31, x5, 100, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -32769, 31, x5, 104, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -65537, 31, x5, 108, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -131073, 31, x5, 112, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -262145, 31, x5, 116, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -524289, 31, x5, 120, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -1048577, 31, x5, 124, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -2097153, 31, x5, 128, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -4194305, 31, x5, 132, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -8388609, 31, x5, 136, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -33554433, 31, x5, 140, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -67108865, 31, x5, 144, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -134217729, 31, x5, 148, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -33, 31, x5, 152, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -268435457, 31, x5, 156, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -536870913, 31, x5, 160, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -1073741825, 31, x5, 164, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 1431655765, 31, x5, 168, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -5, 31, x5, 172, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -1431655766, 31, x5, 176, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -3, 31, x5, 180, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -9, 31, x5, 184, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -17, 31, x5, 188, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -65, 31, x5, 192, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -129, 31, x5, 196, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -257, 31, x5, 200, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -513, 31, x5, 204, x8)
TEST_RR_OP(srl, x12, x10, x11, 1, -1025, 31, x5, 208, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 1073741823, 31, x5, 212, x8)
TEST_RR_OP(srl, x12, x10, x11, 2130706431, -16777217, 0, x5, 216, x8)
TEST_RR_OP(srl, x12, x10, x11, 1073741823, 1073741823, 0, x5, 220, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 16, 16, x5, 224, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 8192, 31, x5, 228, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 32768, 31, x5, 232, x8)
TEST_RR_OP(srl, x12, x10, x11, 0, 131072, 31, x5, 236, x8)
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
    .fill 60*(XLEN/32),4,0xafacadee

RVMODEL_DATA_END
