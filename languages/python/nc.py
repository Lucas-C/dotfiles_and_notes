#!/usr/bin/env python2
# A simple Python 2 equivalent for `nc` command, e.g. to check if a connexion is possible to a remote port
# USAGE: echo HELLO | ./nc.py $host $port
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], int(sys.argv[2])))
print 'Connection OK'
if not sys.stdin.isatty():
    s.sendall(sys.stdin.read())
s.shutdown(socket.SHUT_WR)
while 1:
    data = s.recv(1024)
    if data == "":
        break
    print 'Received:', repr(data)
print 'Connection closed.'
s.close()