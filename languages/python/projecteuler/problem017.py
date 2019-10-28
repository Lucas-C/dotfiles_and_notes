#!/usr/bin/env python3

# If the numbers 1 to 5 are written out in words: one, two, three, four, five,
# then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.
# If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words,
# how many letters would be used?
# NOTE: Do not count spaces or hyphens.
# For example, 342 (three hundred and forty-two) contains 23 letters
# and 115 (one hundred and fifteen) contains 20 letters.
# The use of "and" when writing out numbers is in compliance with British usage.

# L(6-9) = 3 + 5 + 5 + 4 (six, seven, eight, nine) = 17
# L(1-9) = 36
# (ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen)
# => L(10-19) = 3 + 6 + 6 + 8 + 8 + 7 + 7 + 9 + 8 + 8 = 70
# L(20-29) = 10*6 (twenty) + L(1-9) = 96
# L(30-39) = 10*6 (thirty) + L(1-9) = 96
# L(40-49) = 10*5 (forty) + L(1-9) = 96
# L(50-59) = 10*5 (fifty) + L(1-9) = 86
# L(60-69) = 10*5 (sixty) + L(1-9) = 86
# L(70-79) = 10*7 (seventy) + L(1-9) = 106
# L(80-89) = 10*6 (eighty) + L(1-9) = 96
# L(90-99) = 10*6 (ninety) + L(1-9) = 96
# => L(20-99) = 10*(6+6+5+5+5+7+6+6) + 8*L(1-9) = 748
# => L(1-99) = 854
# L(100-199) = 10 + (one hundred) + 99*13 (one hundred and) + L(1-99) = 2161
# L(100-999) = 36+9*7 (hundred) + 99*(36 + 9*10 (hundred and)) + 9*L(1-99) = 20259
# L(1000) = 11 (one thousand)
# => L(1-1000) = L(1-99) + L(100-999) + L(1000) = 21224

import sys

def one2nine():
    return ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

def ten2nineteen():
    return ('ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen')

def one2ninetynine():
    yield from one2nine()
    yield from ten2nineteen()
    for ten in ('twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'):
        yield ten
        for digit in one2nine():
            yield ten + ' ' + digit

def one2onethousand():
    yield from one2ninetynine()
    for hundred in one2nine():
        base = hundred + ' hundred'
        yield base
        base += ' and'
        for digit in one2ninetynine():
            yield base + ' ' + digit
    yield 'one thousand'

if __name__ == '__main__':
    total = 0
    for n in one2onethousand():
        print(n, file=sys.stderr)
        total += sum(1 for c in n if 'a' <= c <= 'z')
    print(total)
