#!/usr/bin/env python3

# The following iterative sequence is defined for the set of positive integers:
#   n → n/2 (n is even)
#   n → 3n + 1 (n is odd)
# Using the rule above and starting with 13, we generate the following sequence:
#   13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
# It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms.
# Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.
# Which starting number, under one million, produces the longest chain?
# NOTE: Once the chain starts the terms are allowed to go above one million.

# time ./problem014.py
# 837799 556
# real    0m5,323s

def collatz(n):
    if n % 2:
        return 3 * n + 1
    return n // 2

if __name__ == '__main__':
    mem = {} # number -> (next, length)
    max_length = 0
    start_for_max_length = None
    for i in range(1,   1000000):
        n, length = i, 1
        while True:
            known_length = mem.get(n)
            if known_length is not None:
                length += known_length
                break
            length += 1
            n = collatz(n)
            if n == 1:
                break
        mem[i] = length
        if length > max_length:
            start_for_max_length, max_length = i, length
    print(start_for_max_length, max_length)
