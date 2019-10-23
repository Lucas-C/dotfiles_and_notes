#!/usr/bin/env python3

# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143 ?

# time ./problem03.py
# 6857
# real    0m0,182s

def test_factors():
    assert factors(13195) == {5, 7, 13, 29}

def factors(n):
    f = set()
    i = 2
    while i * i < n:
        while n % i == 0:
            n = n // i
            f.add(i)
        i += 1
    f.add(n)
    return f

if __name__ == '__main__':
    print(max(factors(600851475143)))
