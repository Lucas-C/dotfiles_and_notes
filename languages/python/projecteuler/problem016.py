#!/usr/bin/env python3

# 2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.
# What is the sum of the digits of the number 2^1000?

# time ./problem016.py
# 1366
# real    0m0,207s

if __name__ == '__main__':
    n = 2**1000
    total = 0
    while n:
        total += n % 10
        n //= 10
    print(total)
