#!/usr/bin/env python3
# A simple Python 3 equivalent for `nc -l` command, e.g. to listen for Graphite logs
# USAGE: ./tcp_listen.py $host $port
import socket, sys
from socketserver import StreamRequestHandler, TCPServer

class RequestHandler(StreamRequestHandler):
    def handle(self):
        print(self.rfile.readline(65537).decode('utf8'), end='')
        self.wfile.flush()

TCPServer((sys.argv[1], int(sys.argv[2])), RequestHandler).serve_forever()
