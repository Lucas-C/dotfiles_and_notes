#!/usr/bin/python3

# Transform some text so that it can be read by reversing the device.
# Inspired by 1337 5|*34|< & calculator spelling
# USAGE: echo -en "ceci est un indice !" | ./letter_reverser.py

import sys

FROM = "ABCDEGHIJLMNOPQSTUVWXYZ!?,'- \n" # missing: F K R
TO   = "e8>P39H127Wu0bb5+n^MXhZ¡¿',- \n"

miss_count = 0
for c in reversed(sys.stdin.read()):
    try:
        i = FROM.index(c.upper())
    except ValueError:
        miss_count += 1
        continue
    print(TO[i], end='')
print()
if miss_count:
    print(f'{miss_count} could not be reversed')
