#!/usr/bin/env python3

# Yes, using those libs seems a bit like cheating, but it's only for testing,
# and anyway it's not enough to brute force this problem under 1min on my machine...
from numba import jit, prange
#from sympy.ntheory import divisors

DIVISORS_GOAL = 500

@jit(nopython=True, parallel=True)
def divisors_count(n):
    count = 2  # 1 & n
    i = 2
    while i * i <= n:
        if n % i == 0:
            count += 1
            if i != n // i:
                count += 1
        i += 1
    return count

@jit(nopython=True, parallel=True)
def main():
    for n in prange(1, 3000000):
        T = n*(n+1)//2
        if divisors_count(T) >= DIVISORS_GOAL:
            return n, T
    return 0, 0

if __name__ == '__main__':
    print(main())
