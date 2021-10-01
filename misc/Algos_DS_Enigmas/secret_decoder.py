#!/usr/bin/python
# USAGE: ./secret_decoder.py 190 < secret_msg.txt > decoded.txt
import sys
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
msg = sys.stdin.read()
print('\n'.join(chunks(msg, int(sys.argv[1]))))