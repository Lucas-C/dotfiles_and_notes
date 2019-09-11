#!/usr/bin/env python3
# By Julien Voisin from issue 1 of Paged Out: https://pagedout.institute
# Good idea, tested on this basic Python program => too slow and does not find the correct flag:
#    #!/usr/bin/python
#    import sys;
#    if sys.argv[1] == 'DEADBEEF':
#        print('FLAG FOUND')
import string, shlex, sys
from subprocess import Popen, PIPE

cmd = 'perf stat -r 25 -x, -e instructions:u %s ' % sys.argv[1]
key =  ''

while True:
    maximum = 0,0
    for i in string.printable:
        c = cmd + shlex.quote(key+i) + ' >/dev/null'
        _, stdout = Popen(c, stderr=PIPE, shell=True).communicate()
        nb_instructions = int(stdout.decode('utf-8').split(',')[0])
        if nb_instructions > maximum[0]:
            maximum = nb_instructions, i
    key += maximum[1]
    print(key)
