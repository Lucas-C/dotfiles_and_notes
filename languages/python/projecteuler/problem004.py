#!/usr/bin/env python3

# A palindromic number reads the same both ways.
# The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
# Find the largest palindrome made from the product of two 3-digit numbers.

# time ./problem04.py
# 993 913 906609
# real    0m0,166s

from itertools import count

def test_is_palindromic():
    assert is_palindromic(9009)
    assert is_palindromic(909)
    assert not is_palindromic(123)

def is_palindromic(n):
    digits = []
    while n:
        digits.append(n % 10)
        n = n // 10
    return digits == list(reversed(digits))

def test_decreasing_biproducts():
    decreasing_biproducts(5) == [(5*5), (5*4), (5*3), (4*4), (5*2), (4*3), (5*1), (4*2), (3*3)]

def decreasing_biproducts(n):
    for diff in count(1):
        for i in range(diff):
            yield n - i, n - diff + i - 1

if __name__ == '__main__':
    for x, y in decreasing_biproducts(999):
        if is_palindromic(x * y):
            print(x, y, x * y)
            break
