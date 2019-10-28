#!/usr/bin/env python3

# Find the maximum total from top to bottom in triangle.txt,
# a 15K text file containing a triangle with one-hundred rows.

# time ./problem067.py
# 7273
# real    0m0,204s

with open('p067_triangle.txt') as triangle_file:
    TRIANGLE = [list(map(int, row.split(' '))) for row in triangle_file.readlines() if row]

if __name__ == '__main__':
    max_sums = list(TRIANGLE[-1])
    for i in reversed(range(1, len(TRIANGLE))):
        new_max_sums = [0] * (len(TRIANGLE[i]) - 1)
        for j in range(len(new_max_sums)):
            new_max_sums[j] = TRIANGLE[i-1][j] + max(max_sums[j], max_sums[j+1])
        max_sums = new_max_sums
    print(max_sums[0])
