#!/usr/bin/env python3

# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9.
# The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.

# time ./problem01.py
# 233168
# real    0m0,143s

def test_sum_multiples_of_n_below_m():
    assert sum_multiples_of_n_below_m(n=3, m=3) == 0
    assert sum_multiples_of_n_below_m(n=3, m=4) == 3
    assert sum_multiples_of_n_below_m(n=3, m=10) == 3+6+9

def sum_multiples_of_n_below_m(n, m):
    N = (m - 1) // n
    return N * (N + 1) // 2 * n

if __name__ == '__main__':
    print(sum_multiples_of_n_below_m(n=3, m=1000) \
        + sum_multiples_of_n_below_m(n=5, m=1000) \
        - sum_multiples_of_n_below_m(n=15, m=1000))
