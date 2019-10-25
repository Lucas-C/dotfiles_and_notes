#!/usr/bin/env python3

# Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down,
# there are exactly 6 routes to the bottom right corner.
# How many such routes are there through a 20×20 grid?

# Notes:
#   #routes(1) = 2
#   #routes(2) = 6
#   #routes(3) = 20
#   #routes(4) = 70
#   #routes(N) = binomial(2*N, N)

try:
    from math import comb  # Python 3.8
except ImportError:
    from math import factorial
    def comb(x, y):
        return factorial(x) // factorial(y) // factorial(x - y)

if __name__ == '__main__':
    for n in range(1, 21):
        print(comb(2*n, n))
