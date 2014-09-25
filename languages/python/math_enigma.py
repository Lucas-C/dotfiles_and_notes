# FROM: http://blog.tanyakhovanova.com/?p=504 - old Olympiad problem
#   "Prove that you can choose 2^k numbers from the set {1, 2, 3, ..., 3^k-1}
#   in such a way that the chosen set contains no averages of any two of its elements."
# My solution:
#   N_0 = {1}
#   N_{k+1} = N_k U {3^k + e | e in N_k}
# Demonstration by induction, using the property that for every element e of N_k, e <= (3^k+1)/2

from __future__ import print_function
import sys

def main():
    assert can_be_added(1, [])
    assert not can_be_added(3, [1,2])

    k = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    N = set()
    for p in xrange(1, 3**k):
        if can_be_added(p, N):
            N.add(p)
    print(sorted(N), "length:", len(N))

def can_be_added(p, N):
    # An element can only be added iff added to any element in N, their sum isn't also in N
    for e in N:
        added = e + p
        if added & 1: # is odd
            continue
        if (added / 2) in N:
            return False
    return True

if __name__ == '__main__':
    main()
