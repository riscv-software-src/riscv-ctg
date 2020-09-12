
#include "compliance_model.h"
#include "compliance_test.h"

RVTEST_ISA("RV32I")

RVMODEL_BOOT
RVTEST_CODE_BEGIN

#ifdef TEST_CASE_1
RVTEST_CASE(1,"//check ISA:=regex(.*I.*);def TEST_CASE_1=True;",sltiu)
la x1,signature_x1_1
TEST_IMM_OP( sltiu, x31, x31, 0, 2048, 2048, x1, 0, x2)
TEST_IMM_OP( sltiu, x30, x29, 0, 4160749567, 4095, x1, 4, x2)
TEST_IMM_OP( sltiu, x29, x30, 1, 0, 4095, x1, 8, x2)
TEST_IMM_OP( sltiu, x28, x27, 0, 4294967295, 4095, x1, 12, x2)
TEST_IMM_OP( sltiu, x27, x28, 1, 1, 4095, x1, 16, x2)
TEST_IMM_OP( sltiu, x26, x25, 0, 4160749567, 0, x1, 20, x2)
TEST_IMM_OP( sltiu, x25, x26, 0, 4160749567, 1, x1, 24, x2)
TEST_IMM_OP( sltiu, x24, x23, 1, 2, 4095, x1, 28, x2)
TEST_IMM_OP( sltiu, x23, x24, 1, 4, 4095, x1, 32, x2)
TEST_IMM_OP( sltiu, x22, x21, 1, 8, 4095, x1, 36, x2)
TEST_IMM_OP( sltiu, x21, x22, 1, 16, 4095, x1, 40, x2)
TEST_IMM_OP( sltiu, x20, x19, 1, 32, 4095, x1, 44, x2)
TEST_IMM_OP( sltiu, x19, x20, 1, 64, 4095, x1, 48, x2)
TEST_IMM_OP( sltiu, x18, x17, 1, 128, 4095, x1, 52, x2)
TEST_IMM_OP( sltiu, x17, x18, 1, 256, 4095, x1, 56, x2)
TEST_IMM_OP( sltiu, x16, x15, 1, 512, 4095, x1, 60, x2)
TEST_IMM_OP( sltiu, x15, x16, 1, 1024, 4095, x1, 64, x2)
TEST_IMM_OP( sltiu, x14, x13, 0, 4096, 4095, x1, 68, x2)
TEST_IMM_OP( sltiu, x13, x14, 0, 8192, 4095, x1, 72, x2)
TEST_IMM_OP( sltiu, x12, x11, 0, 16384, 4095, x1, 76, x2)
TEST_IMM_OP( sltiu, x11, x12, 0, 32768, 4095, x1, 80, x2)
TEST_IMM_OP( sltiu, x10, x9, 0, 65536, 4095, x1, 84, x2)
TEST_IMM_OP( sltiu, x9, x10, 0, 131072, 4095, x1, 88, x2)
TEST_IMM_OP( sltiu, x8, x7, 0, 262144, 4095, x1, 92, x2)
TEST_IMM_OP( sltiu, x7, x8, 0, 524288, 4095, x1, 96, x2)
TEST_IMM_OP( sltiu, x6, x5, 0, 1048576, 4095, x1, 100, x2)
TEST_IMM_OP( sltiu, x5, x6, 0, 2097152, 4095, x1, 104, x7)
TEST_IMM_OP( sltiu, x4, x3, 0, 4194304, 4095, x1, 108, x7)
la x5,signature_x5_0
TEST_IMM_OP( sltiu, x3, x4, 0, 8388608, 4095, x5, 0, x7)
TEST_IMM_OP( sltiu, x2, x1, 0, 16777216, 4095, x5, 4, x7)
TEST_IMM_OP( sltiu, x1, x2, 0, 33554432, 4095, x5, 8, x7)
TEST_IMM_OP( sltiu, x31, x0, 0, 67108864, 4095, x5, 12, x7)
TEST_IMM_OP( sltiu, x0, x31, 0, 134217728, 4095, x5, 16, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 268435456, 4095, x5, 20, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 536870912, 4095, x5, 24, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 1073741824, 4095, x5, 28, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 2147483648, 4095, x5, 32, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967294, 4095, x5, 36, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967293, 4095, x5, 40, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967291, 4095, x5, 44, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967287, 4095, x5, 48, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967279, 4095, x5, 52, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967263, 4095, x5, 56, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967231, 4095, x5, 60, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967167, 4095, x5, 64, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294967039, 4095, x5, 68, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294966783, 4095, x5, 72, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294966271, 4095, x5, 76, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294965247, 4095, x5, 80, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294963199, 4095, x5, 84, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294959103, 4095, x5, 88, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294950911, 4095, x5, 92, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294934527, 4095, x5, 96, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294901759, 4095, x5, 100, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294836223, 4095, x5, 104, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294705151, 4095, x5, 108, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4294443007, 4095, x5, 112, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4293918719, 4095, x5, 116, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4292870143, 4095, x5, 120, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4290772991, 4095, x5, 124, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4286578687, 4095, x5, 128, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4278190079, 4095, x5, 132, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4261412863, 4095, x5, 136, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4227858431, 4095, x5, 140, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4026531839, 4095, x5, 144, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 3758096383, 4095, x5, 148, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 3221225471, 4095, x5, 152, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 2147483647, 4095, x5, 156, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 1431655765, 4095, x5, 160, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 2863311530, 4095, x5, 164, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 2, x5, 168, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4, x5, 172, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 8, x5, 176, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 16, x5, 180, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 32, x5, 184, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 64, x5, 188, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 128, x5, 192, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 256, x5, 196, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 512, x5, 200, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 1365, x5, 204, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 2730, x5, 208, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 1024, x5, 212, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4094, x5, 216, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4093, x5, 220, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4091, x5, 224, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4087, x5, 228, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4079, x5, 232, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4063, x5, 236, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 4031, x5, 240, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 3967, x5, 244, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 3839, x5, 248, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 3583, x5, 252, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 3071, x5, 256, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 4160749567, 2047, x5, 260, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 2048, 2048, x5, 264, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 67108864, 4095, x5, 268, x7)
TEST_IMM_OP( sltiu, x11, x10, 0, 134217728, 4095, x5, 272, x7)
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
    .fill 69*(XLEN/32),4,0xafacadee

RVMODEL_DATA_END
