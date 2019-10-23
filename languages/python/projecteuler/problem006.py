#!/usr/bin/env python3

# The sum of the squares of the first ten natural numbers is,
#   1² + 2² + ... + 10² = 385
# The square of the sum of the first ten natural numbers is,
#  (1 + 2 + ... + 10)² = 55² = 3025
# Hence the difference between the sum of the squares of the first ten natural numbers
# and the square of the sum is 3025 − 385 = 2640.
# Find the difference between the sum of the squares of the first one hundred natural numbers
# and the square of the sum.

# time ./problem06.py
# 25164150
# real    0m0,136s

if __name__ == '__main__':
    print(sum(i for i in range(1, 101))**2 \
          - sum(i*i for i in range(1, 101)))
