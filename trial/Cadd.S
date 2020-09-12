
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32IC")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*C.*);def TEST_CASE_1=True;",cadd)
la x1,signature_x1_1
TEST_CR_OP( c.add, x30, x31, 0, -16777217, 1073741823, x1, 0, x2)
TEST_CR_OP( c.add, x29, x29, 0, -16777217, -16777217, x1, 4, x2)
TEST_CR_OP( c.add, x31, x30, 0, -2147483648, -16777217, x1, 8, x2)
TEST_CR_OP( c.add, x27, x28, 0, 0, -16777217, x1, 12, x2)
TEST_CR_OP( c.add, x28, x27, 0, 2147483647, -16777217, x1, 16, x2)
TEST_CR_OP( c.add, x25, x26, 0, 1, -16777217, x1, 20, x2)
TEST_CR_OP( c.add, x26, x25, 0, -16777217, -2147483648, x1, 24, x2)
TEST_CR_OP( c.add, x23, x24, 0, -16777217, 0, x1, 28, x2)
TEST_CR_OP( c.add, x24, x23, 0, -16777217, 2147483647, x1, 32, x2)
TEST_CR_OP( c.add, x21, x22, 0, -16777217, 1, x1, 36, x2)
TEST_CR_OP( c.add, x22, x21, 0, 2, -16777217, x1, 40, x2)
TEST_CR_OP( c.add, x19, x20, 0, 4, -16777217, x1, 44, x2)
TEST_CR_OP( c.add, x20, x19, 0, 8, -16777217, x1, 48, x2)
TEST_CR_OP( c.add, x17, x18, 0, 16, -16777217, x1, 52, x2)
TEST_CR_OP( c.add, x18, x17, 0, 32, -16777217, x1, 56, x2)
TEST_CR_OP( c.add, x15, x16, 0, 64, -16777217, x1, 60, x2)
TEST_CR_OP( c.add, x16, x15, 0, 128, -16777217, x1, 64, x2)
TEST_CR_OP( c.add, x13, x14, 0, 256, -16777217, x1, 68, x2)
TEST_CR_OP( c.add, x14, x13, 0, 512, -16777217, x1, 72, x2)
TEST_CR_OP( c.add, x11, x12, 0, 1024, -16777217, x1, 76, x2)
TEST_CR_OP( c.add, x12, x11, 0, 2048, -16777217, x1, 80, x2)
TEST_CR_OP( c.add, x9, x10, 0, 4096, -16777217, x1, 84, x2)
TEST_CR_OP( c.add, x10, x9, 0, 8192, -16777217, x1, 88, x2)
TEST_CR_OP( c.add, x7, x8, 0, 16384, -16777217, x1, 92, x2)
TEST_CR_OP( c.add, x8, x7, 0, 32768, -16777217, x1, 96, x2)
TEST_CR_OP( c.add, x5, x6, 0, 65536, -16777217, x1, 100, x2)
TEST_CR_OP( c.add, x6, x5, 0, 131072, -16777217, x1, 104, x7)
TEST_CR_OP( c.add, x3, x4, 0, 262144, -16777217, x1, 108, x7)
la x5,signature_x5_0
TEST_CR_OP( c.add, x4, x3, 0, 524288, -16777217, x5, 0, x7)
TEST_CR_OP( c.add, x1, x2, 0, 1048576, -16777217, x5, 4, x7)
TEST_CR_OP( c.add, x2, x1, 0, 2097152, -16777217, x5, 8, x7)
TEST_CR_OP( c.add, x0, x31, 0, 4194304, -16777217, x5, 12, x7)
TEST_CR_OP( c.add, x10, x11, 0, 8388608, -16777217, x5, 16, x7)
TEST_CR_OP( c.add, x10, x11, 0, 16777216, -16777217, x5, 20, x7)
TEST_CR_OP( c.add, x10, x11, 0, 33554432, -16777217, x5, 24, x7)
TEST_CR_OP( c.add, x10, x11, 0, 67108864, -16777217, x5, 28, x7)
TEST_CR_OP( c.add, x10, x11, 0, 134217728, -16777217, x5, 32, x7)
TEST_CR_OP( c.add, x10, x11, 0, 268435456, -16777217, x5, 36, x7)
TEST_CR_OP( c.add, x10, x11, 0, 536870912, -16777217, x5, 40, x7)
TEST_CR_OP( c.add, x10, x11, 0, 1073741824, -16777217, x5, 44, x7)
TEST_CR_OP( c.add, x10, x11, 0, -2, -16777217, x5, 48, x7)
TEST_CR_OP( c.add, x10, x11, 0, -3, -16777217, x5, 52, x7)
TEST_CR_OP( c.add, x10, x11, 0, -5, -16777217, x5, 56, x7)
TEST_CR_OP( c.add, x10, x11, 0, -9, -16777217, x5, 60, x7)
TEST_CR_OP( c.add, x10, x11, 0, -17, -16777217, x5, 64, x7)
TEST_CR_OP( c.add, x10, x11, 0, -33, -16777217, x5, 68, x7)
TEST_CR_OP( c.add, x10, x11, 0, -65, -16777217, x5, 72, x7)
TEST_CR_OP( c.add, x10, x11, 0, -129, -16777217, x5, 76, x7)
TEST_CR_OP( c.add, x10, x11, 0, -257, -16777217, x5, 80, x7)
TEST_CR_OP( c.add, x10, x11, 0, -513, -16777217, x5, 84, x7)
TEST_CR_OP( c.add, x10, x11, 0, -1025, -16777217, x5, 88, x7)
TEST_CR_OP( c.add, x10, x11, 0, -2049, -16777217, x5, 92, x7)
TEST_CR_OP( c.add, x10, x11, 0, -4097, -16777217, x5, 96, x7)
TEST_CR_OP( c.add, x10, x11, 0, -8193, -16777217, x5, 100, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16385, -16777217, x5, 104, x7)
TEST_CR_OP( c.add, x10, x11, 0, -32769, -16777217, x5, 108, x7)
TEST_CR_OP( c.add, x10, x11, 0, -65537, -16777217, x5, 112, x7)
TEST_CR_OP( c.add, x10, x11, 0, -131073, -16777217, x5, 116, x7)
TEST_CR_OP( c.add, x10, x11, 0, -262145, -16777217, x5, 120, x7)
TEST_CR_OP( c.add, x10, x11, 0, -524289, -16777217, x5, 124, x7)
TEST_CR_OP( c.add, x10, x11, 0, -1048577, -16777217, x5, 128, x7)
TEST_CR_OP( c.add, x10, x11, 0, -2097153, -16777217, x5, 132, x7)
TEST_CR_OP( c.add, x10, x11, 0, -4194305, -16777217, x5, 136, x7)
TEST_CR_OP( c.add, x10, x11, 0, -8388609, -16777217, x5, 140, x7)
TEST_CR_OP( c.add, x10, x11, 0, -33554433, -16777217, x5, 144, x7)
TEST_CR_OP( c.add, x10, x11, 0, -67108865, -16777217, x5, 148, x7)
TEST_CR_OP( c.add, x10, x11, 0, -134217729, -16777217, x5, 152, x7)
TEST_CR_OP( c.add, x10, x11, 0, -268435457, -16777217, x5, 156, x7)
TEST_CR_OP( c.add, x10, x11, 0, -536870913, -16777217, x5, 160, x7)
TEST_CR_OP( c.add, x10, x11, 0, -1073741825, -16777217, x5, 164, x7)
TEST_CR_OP( c.add, x10, x11, 0, 1431655765, -16777217, x5, 168, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -4194305, x5, 172, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -8388609, x5, 176, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -33554433, x5, 180, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -67108865, x5, 184, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -134217729, x5, 188, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -268435457, x5, 192, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -536870913, x5, 196, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -1073741825, x5, 200, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 1431655765, x5, 204, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -1431655766, x5, 208, x7)
TEST_CR_OP( c.add, x10, x11, 0, -1431655766, -16777217, x5, 212, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 2, x5, 216, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 4, x5, 220, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 8, x5, 224, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 16, x5, 228, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 32, x5, 232, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 64, x5, 236, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 128, x5, 240, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 256, x5, 244, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 512, x5, 248, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 1024, x5, 252, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 2048, x5, 256, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 4096, x5, 260, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 8192, x5, 264, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 16384, x5, 268, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 32768, x5, 272, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 65536, x5, 276, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 131072, x5, 280, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 262144, x5, 284, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 524288, x5, 288, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 1048576, x5, 292, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 2097152, x5, 296, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 4194304, x5, 300, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 8388608, x5, 304, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 16777216, x5, 308, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 33554432, x5, 312, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 67108864, x5, 316, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 134217728, x5, 320, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 268435456, x5, 324, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 536870912, x5, 328, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, 1073741824, x5, 332, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -2, x5, 336, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -3, x5, 340, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -5, x5, 344, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -9, x5, 348, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -17, x5, 352, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -33, x5, 356, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -65, x5, 360, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -129, x5, 364, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -257, x5, 368, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -513, x5, 372, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -1025, x5, 376, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -2049, x5, 380, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -4097, x5, 384, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -8193, x5, 388, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -16385, x5, 392, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -32769, x5, 396, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -65537, x5, 400, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -131073, x5, 404, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -262145, x5, 408, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -524289, x5, 412, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -1048577, x5, 416, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -2097153, x5, 420, x7)
TEST_CR_OP( c.add, x10, x11, 0, -16777217, -16777217, x5, 424, x7)
TEST_CR_OP( c.add, x10, x11, 0, 4194304, -16777217, x5, 428, x7)
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
    .fill 108*(XLEN/32),4,0xafacadee

RVMODEL_DATA_END
