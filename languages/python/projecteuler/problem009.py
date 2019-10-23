#!/usr/bin/env python3

# A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
#   a² + b² = c²
# For example, 3² + 4² = 9 + 16 = 25 = 5².
# There exists exactly one Pythagorean triplet for which a + b + c = 1000.
# Find the product abc.

# time ./problem09.py
# 31875000
# real    0m1,048s

if __name__ == '__main__':
    for a in range(1, 1000):
        for b in range(1, 1000):
            c = 1000 - a - b
            if a*a + b*b == c*c:
                print(a, b, c)
                print(a * b * c)
                exit(0)
