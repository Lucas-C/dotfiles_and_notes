#!/usr/bin/env python3

# A natural number, N, that can be written as the sum and product of a given set of at least two natural numbers,
# {a1, a2, ... , ak} is called a product-sum number: N = a1 + a2 + ... + ak = a1 × a2 × ... × ak.
# For example, 6 = 1 + 2 + 3 = 1 × 2 × 3.
# For a given set of size, k, we shall call the smallest N with this property a minimal product-sum number.
# The minimal product-sum numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.
#   k=2: 4 = 2 × 2 = 2 + 2
#   k=3: 6 = 1 × 2 × 3 = 1 + 2 + 3
#   k=4: 8 = 1 × 1 × 2 × 4 = 1 + 1 + 2 + 4
#   k=5: 8 = 1 × 1 × 2 × 2 × 2 = 1 + 1 + 2 + 2 + 2
#   k=6: 12 = 1 × 1 × 1 × 1 × 2 × 6 = 1 + 1 + 1 + 1 + 2 + 6
# Hence for 2≤k≤6, the sum of all the minimal product-sum numbers is 4+6+8+12 = 30;
# note that 8 is only counted once in the sum.
# In fact, as the complete set of minimal product-sum numbers for 2≤k≤12 is {4, 6, 8, 12, 15, 16}, the sum is 61.
# What is the sum of all the minimal product-sum numbers for 2≤k≤12000?

# LEMMES:
#  - N(k) > k                                       (trivial)
#  - N(k) <= 2*k                                    (unproved)
#  - for all k factors f_i composing N(k), f_i <= k (stem from above one, by absurd)
#  - the number of factors f_i>=2 composing N(k)
#    is lower than log2(k)                          (trivial, by absurd)

#   k=7: 12 = 1 × 1 × 1 × 1 × 3 x 4 = 1 + 1 + 1 + 1 + 1 + 3 + 4
#   k=8: 16 = 1 × 1 × 1 × 1 × 1 × 2 x 8 = 1 + 1 + 1 + 1 + 1 + 1 + 2 + 8
#   k=9: 15 = 1 × 1 × 1 × 1 × 1 × 1 × 3 x 5 = 1 + 1 + 1 + 1 + 1 + 1 + 1 + 3 + 5
#   k=60: 72 = 1 × 1 x ... x 2 x 4 x 9 = 1 + 1 + ... + 2 + 4 + 9
#   k=444: 888 = 1 × 1 x ... x 2 x 444 = 1 + 1 + ... + 2 + 444

# time ./problem88.py
#-> NOT SOLVED YET, too slow... -> must re-think diffs-to-product table build logic?

import sys
from functools import reduce
from itertools import count
from math import floor, log2

MAX_K = 1500                      # takes around 48s to complete... we are far from reaching MAX_K=12000 :(
                                  # the bottleneck is clearly the diffs-to-product building phase
MAX_FACTORS = floor(log2(MAX_K))  # exclusive max number of factors of ALL N(k) products, ignoring x1
MAX_VALUE = MAX_K                 # max factor value
print('MAX_FACTORS=%s' % MAX_FACTORS)

def test_product_total_combinations():
    global MAX_VALUE
    MAX_VALUE=4
    assert list(product_total_combinations(2, 2)) == [
        (2*2, 2+2),
        (2*3, 2+3),
        (2*4, 2+4),
        (3*3, 3+3),
        (3*4, 3+4),
        (4*4, 4+4),
    ]
    MAX_VALUE=3
    assert list(product_total_combinations(2, 3)) == [
        (2*2*2, 2+2+2),
        (2*2*3, 2+2+3),
        (2*3*3, 2+3+3),
        (3*3*3, 3+3+3),
    ]
    MAX_VALUE=5
    global UPPER_BOUND
    UPPER_BOUND = 9
    assert list(product_total_combinations(2, 2)) == [
        (2*2, 2+2),
        (2*3, 2+3),
        (2*4, 2+4),
        (3*3, 3+3),
    ]

STORE_FACTORS = False  # ease debugging, else store only their product, which is a lot more memory efficient
def product_from(stored):
    return reduce((lambda x, y: x * y), stored) if STORE_FACTORS else stored

UPPER_BOUND = 2*MAX_VALUE
MAX_DIFF = MAX_VALUE
#@lru_cache(maxsize=MAX_FACTORS*MAX_VALUE)  # not a good idea, actually makes the program slower
def product_total_combinations(start, seq_length, product=1, total=0):
    '''
    Like itertools.combinations_with_replacement,
    but does not iterate over sequences whose product or sum is above UPPER_BOUND,
    or whose (product - sum) difference is above MAX_DIFF,
    and only yield (product, total).
    Why ?
    Because #combinations_with_replacement of R items among N is: (R+N−1)!/R!(N−1)!
    (this is the binomial coefficient "R+N-1 choose R")
    For R=14 and N=12000, the result is above 10^10000 :(
    Hence we use this custom iterator, with a bounded max value for the products/totals, and their diff.
    '''
    if product > UPPER_BOUND or total > UPPER_BOUND or (product - total) > MAX_DIFF:
        return
    if seq_length == 0:
        yield (product, total)
        return
    for i in range(start, MAX_VALUE+1):
        yield from product_total_combinations(i, seq_length-1, product*i, total+i)

if STORE_FACTORS:  # override above function to returns factors instead of only their product:
    def product_total_combinations(start, seq_length, factors=(), total=0):
        if factors:
            product = product_from(factors)
            if product > UPPER_BOUND or total > UPPER_BOUND or (product - total) > MAX_DIFF:
                return
        if seq_length == 0:
            yield (factors, total)
            return
        for i in range(start, MAX_VALUE+1):
            yield from product_total_combinations(i, seq_length-1, factors+(i,), total+i)

if __name__ == '__main__':
    diffs_to_product = {}  # factors_count -> { (product-sum) -> product }
    for factors_count in range(2, MAX_FACTORS+1):
        diff_to_product = {}
        for stored, total in product_total_combinations(start=2, seq_length=factors_count):
            product = product_from(stored)
            diff = product - total
            if diff not in diff_to_product or product < product_from(diff_to_product[diff]):
                diff_to_product[diff] = stored
        diffs_to_product[factors_count] = diff_to_product
        print('Built diff-to-product table of length %s for #factors=%s' % (len(diff_to_product), factors_count), file=sys.stderr)
    all_Nks = set()
    max_Nk_minus_k, special_k = 0, None
    for k in range(2, MAX_K+1):
        min_product, optimal_factors_count, optimal_factors = None, None, None
        for factors_count in range(2, k+1):
            sum_of_ones = k - factors_count
            if factors_count not in diffs_to_product:
                if min_product is None:
                    raise RuntimeError('MAX_FACTORS or MAX_VALUE is too low ! (k=%s)' % k)
                break  # not sure why it's OK, naively we should `continue`
            if sum_of_ones in diffs_to_product[factors_count]:
                stored = diffs_to_product[factors_count][sum_of_ones]
                product = product_from(stored)
                if min_product is None or product < min_product:
                    min_product, optimal_factors_count, optimal_factors = product, factors_count, stored
        print('N(k=%s)=%s - #factors=%s' % (k, min_product, optimal_factors_count), file=sys.stderr)
        if STORE_FACTORS:
            print('  factors:', optimal_factors, file=sys.stderr)
        all_Nks.add(min_product)
        if min_product - k > max_Nk_minus_k:
            max_Nk_minus_k, special_k = min_product - k, k
    print('Max(N(k)-k)=%s for k=%s' % (max_Nk_minus_k, special_k), file=sys.stderr)
    print(sum(all_Nks))
