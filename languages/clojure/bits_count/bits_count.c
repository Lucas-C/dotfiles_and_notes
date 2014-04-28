// FROM: http://graphics.stanford.edu/~seander/bithacks.html

#include "stdio.h"
#include "limits.h"
#include "stdint.h"
#include "inttypes.h"

#define STR(x) #x
#define STRINGIFY(x) STR(x)

#define MASK1(T) (T)~(T)0/3
#define MASK2(T) (T)~(T)0/5
#define MASK3(T) (T)~(T)0/17
#define MASK4(T) ((T)~(T)0/255)

#define BITS_COUNT(T, v, c) \
    v = v - ((v >> 1) & MASK1(T)); \
    v = (v & MASK2(T)) + ((v >> 2) & MASK2(T)); \
    v = (v + (v >> 4)) & MASK3(T); \
    c = (T)(v * MASK4(T)) >> (sizeof(T) - 1) * CHAR_BIT

#define MAKE_BITS_COUNT_TEST_(BitsSize, UVarType, VarType, PrintFormatI, PrintfFormatU, PrintFormatX) void bits_count_test_##BitsSize##b(UVarType input) {\
    UVarType v = input; \
    UVarType c; \
    printf(STRINGIFY(UVarType)" : v= %"PrintFormatI" / u:%"PrintfFormatU" / 0x%"PrintFormatX, (VarType)v, v, v); \
    BITS_COUNT(UVarType, v, c); \
    printf(" -> c=%"PrintfFormatU"\n", c); \
}

#define MAKE_BITS_COUNT_TEST(BitsSize) MAKE_BITS_COUNT_TEST_(BitsSize, uint##BitsSize##_t, int##BitsSize##_t, PRIi##BitsSize, PRIu##BitsSize, PRIx##BitsSize)

#define PRINT_MASKS_(BitsSize, UVarType, PrintFormatX) \
    printf(STRINGIFY(BitsSize)"bits: MASK1=0x%"PrintFormatX" - MASK2=0x%"PrintFormatX" - MASK3=0x%"PrintFormatX" - MASK4=0x%"PrintFormatX"\n", \
            MASK1(UVarType), MASK2(UVarType), MASK3(UVarType), MASK4(UVarType))

#define PRINT_MASKS(BitsSize) PRINT_MASKS_(BitsSize, uint##BitsSize##_t, PRIx##BitsSize)

MAKE_BITS_COUNT_TEST(8)
MAKE_BITS_COUNT_TEST(16)
MAKE_BITS_COUNT_TEST(32)
MAKE_BITS_COUNT_TEST(64)

int main() {
    PRINT_MASKS(8);
    PRINT_MASKS(16);
    PRINT_MASKS(32);
    PRINT_MASKS(64);

//    bits_count_test_8b(-1);
//    bits_count_test_8b(42);
//    bits_count_test_16b(-1);
//    bits_count_test_16b(42);
    bits_count_test_32b(-1);
    bits_count_test_32b(42);
    bits_count_test_32b(256);
    bits_count_test_64b(-1);
}
