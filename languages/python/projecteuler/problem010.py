#!/usr/bin/env python3

# The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
# Find the sum of all the primes below two million.

# time ./problem10.py
# 142913828922
# real    0m1,694s

import sys
from problem007 import build_prime_sieve, primes_from

if __name__ == '__main__':
    prime_sieve = build_prime_sieve(2000000)
    primes_count = prime_sieve.count(True)
    print('Sieve primes count:', primes_count, file=sys.stderr)
    print('Sieve size in memory: %sb' % prime_sieve.buffer_info()[1], file=sys.stderr)
    print(sum(primes_from(prime_sieve)))
