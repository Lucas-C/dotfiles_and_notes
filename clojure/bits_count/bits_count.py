#!/usr/bin/python

# !! Precedence of '&' and '+' operators are inversed between C & Python

# !! In Python, even if both are of type 'int', -1 != 0xffffffff
# Anyway Python use BigInts and makes no difference whatsoever beyween int & long (they disappear in v3)

def count_bits(v):
    # option 1, for at most 14-bit values in v:
#    c = (v * 0x200040008001 & 0x111111111111111) % 0xf;

    # option 2, for at most 24-bit values in v:
#    c =  ((v & 0xfff) * 0x1001001001001 & 0x84210842108421) % 0x1f;
#    c += (((v & 0xfff000) >> 12) * 0x1001001001001 & 0x84210842108421) % 0x1f;

    # option 3, for at most 32-bit values in v:
    c =  ((v & 0xfff) * 0x1001001001001 & 0x84210842108421) % 0x1f;
    c += (((v & 0xfff000) >> 12) * 0x1001001001001 & 0x84210842108421) % 0x1f;
    c += ((v >> 24) * 0x1001001001001 & 0x84210842108421) % 0x1f;
    return c

assert count_bits(0) == 0
assert count_bits(10) == 2
assert count_bits(0xffffffff) == 32

