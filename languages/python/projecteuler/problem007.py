#!/usr/bin/env python3

# By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.
# What is the 10 001st prime number?

# time ./problem07.py
# 104743
# real    0m0,221s

import math, sys
from bitarray import bitarray

def test_build_prime_sieve():
    prime_sieve = build_prime_sieve(10)
    assert not prime_sieve[0]
    assert not prime_sieve[1]
    assert prime_sieve[2]
    assert prime_sieve[3]
    assert not prime_sieve[4]
    assert prime_sieve[5]
    assert not prime_sieve[6]
    assert prime_sieve[7]
    assert not prime_sieve[8]
    assert not prime_sieve[9]

def build_prime_sieve(n):
    sieve = bitarray(n)
    sieve.setall(True)
    sieve[0], sieve[1] = False, False
    for i in range(2, math.ceil(n**.5)):
        if sieve[i]:
            for j in range(i*i, n, +i):
                sieve[j] = False
    return sieve

if __name__ == '__main__':
    # First, build a sieve big enough to contain 10 001 primes:
    prime_sieve = build_prime_sieve(104750)  # this size is a guess refined by tests
    primes_count = prime_sieve.count(True)
    assert primes_count >= 10001
    print('Sieve primes count:', primes_count, file=sys.stderr)
    print('Sieve size in memory: %sb' % prime_sieve.buffer_info()[1], file=sys.stderr)
    # Second, find 10 001st prime:
    i = 0
    last_prime = None
    for n, is_prime in enumerate(prime_sieve):
        if is_prime:
            last_prime = n
            i += 1
            if i == 10001:
                break
    print(last_prime)
