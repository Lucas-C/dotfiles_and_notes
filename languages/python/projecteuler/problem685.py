#!/usr/bin/env python3

# Writing down the numbers which have a digit sum of 10 in ascending order, we get:
# 19,28,37,46,55,64,73,82,91,109,118,…
# Let f(n,m) be the mth occurrence of the digit sum n. For example, f(10,1)=19, f(10,10)=109 and f(10,100)=1423.
# Let S(k)=∑n=1->k f(n^3,n^4). For example S(3)=7128 and S(10)≡32287064 mod 1000000007.
# Find S(10000) modulo 1000000007.

# Notes:
#  S(k+1) = S(k) + f((k+1)^3, (k+1)^4)
#  f(n, 1) == (str(n % 9) if n % 9 else '') + (n // 9 * '9')

# time ./problem665.py
#-> NOT SOLVED YET, too slow...

from itertools import count
import sys

MOD = 1000000007  # cf. https://www.geeksforgeeks.org/modulo-1097-1000000007/

def test_f():                 #                seuil avant 3 chiffres  - seuil avant 4 chiffres  - seuil avant 5 chiffres
    assert f(7, 8) == 70      #                8
    assert f(7, 9) == 106     #                           +28->
    assert f(7, 14) == 151
    assert f(7, 15) == 160
    assert f(7, 16) == 205
    assert f(7, 36) == 700    #                                          36
    assert f(7, 37) == 1006   #                                                      +84->
    assert f(7, 120) == 7000  #                                                                    120
    assert f(7, 121) == 10006 #
    assert f(8, 9) == 80      #                9
    assert f(8, 10) == 107    #
    assert f(8, 16) == 161    #                           +36->
    assert f(8, 45) == 800    #                                          45
    assert f(8, 46) == 1007   #                                                      +120->
    assert f(8, 165) == 8000  #                                                                    165
    assert f(8, 166) == 10007 #
    assert f(9, 1) == 9       #
    assert f(9, 10) == 90     #                10
    assert f(9, 11) == 108    # '1'+f(9, 1)               +45->
    assert f(9, 55) == 900    #                                          55
    assert f(9, 56) == 1008   # '1'+f(9, 1)                                           +165->
    assert f(9, 220) == 9000  #                                                                    220
    assert f(9, 221) == 10008 # '1'+f(9, 1)
    assert f(10, 1) == 19     #
    assert f(10, 9) == 91     #                9
    assert f(10, 10) == 109   # '1'+f(9, 1)               +54->
    assert f(10, 63) == 910   #                                          63
    assert f(10, 64) == 1009  # '1'+f(9, 1)                                          +219->
    assert f(10, 282) == 9100 #                                                                    282
    assert f(10, 283) == 10009# '1'+f(9, 1)
    assert f(10, 100) == 1423 #
    assert f(11, 1) == 29     #
    assert f(11, 8) == 92     #                8
    assert f(11, 9) == 119    # '1'+f(10, 1)              +61->
    assert f(11, 17) == 191   #
    assert f(11, 18) == 209   #
    assert f(11, 69) == 920   #                                          69
    assert f(11, 70) == 1019  # '1'+f(10, 1)                                         +279->
    assert f(11, 348) == 9200 #                                                                    348
    assert f(11, 349) == 10019# '1'+f(10, 1)
    assert f(18, 1) == 99     #                1
    assert f(19, 1) == 199    # '1'+f(18, 1)
    assert f(19, 2) == 289    # '2'+f(17, 1)
    assert f(19, 3) == 298
    assert f(19, 4) == 379    # '3'+f(16, 1)
    assert f(19, 45) == 991
    assert f(19, 46) == 1099
    assert f(20, 1) == 299
    assert f(20, 37) == 1199
    assert f(20, 38) == 1289
    assert f(26, 1) == 899
    assert f(27, 1) == 999
    assert f(27, 2) == 1899   # '1'+f(26, 1)
    assert f(27, 3) == 1989
    assert f(27, 4) == 1998
    assert f(27, 5) == 2799   # '2'+f(25, 1)
    assert f(27, 6) == 2889
    assert f(27, 7) == 2898
    assert f(27, 81) == 6966

def f(n, m):
    # return f_naive(n, m)
    return int(f_str(n, m))

def f_str(n, m):
    r = (str(n % 9) if n % 9 else '') + (n // 9 * '9')  # f(n, 1)
    for _ in range(1, m):
        lower_digit_pos, lower_digit = next((len(r)-i-1, k) for i, k in enumerate(r[::-1]) if k != '0')
        if lower_digit_pos == 0:  # we grow the string
            assert n < 10
            r = '1' + str(n - 1).zfill(len(r))
        else:
            try:
                prev_non9_digit_pos, prev_non9_digit = next((len(r[:lower_digit_pos])-i-1, k) for i, k in enumerate(r[lower_digit_pos-1::-1]) if k != '9')
                new_digit_value = int(prev_non9_digit) + 1
                left_digits_sum = sum(map(int, r[:prev_non9_digit_pos])) + new_digit_value
                r = r[:prev_non9_digit_pos] + str(new_digit_value) + f_str(n-left_digits_sum, 1).zfill(len(r) - prev_non9_digit_pos - 1)
            except StopIteration:  # there are only 9s on the left
                r = '1' + f_str(n-1, 1).zfill(len(r))
    return r

def f_naive(n, m):
    i = 0
    for k in count(1):
        if sum_digits(k) == n:
            i += 1
            if i == m:
                return k

def sum_digits(k):
    t = 0
    while k:
        t += k % 10
        k //= 10
    return t

if __name__ == '__main__':
    S = 0
    for i in range(1, 10000):
        S += f(i**3, i**4)
        S %= MOD
        print(S, file=sys.stderr)
        if i == 3:
            assert S == 7128
        if i == 10:
            assert S == 32287064
    print(S)
