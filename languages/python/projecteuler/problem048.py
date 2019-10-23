#!/usr/bin/env python3

# The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
# Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.

# time ./problem48.py

if __name__ == '__main__':
    print(sum(i**i for i in range(1, 1001)) % 10000000000)
