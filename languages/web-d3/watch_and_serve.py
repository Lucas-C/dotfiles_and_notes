#!/usr/bin/env python3
from livereload import Server

server = Server()
server.watch('*.html')
server.watch('*.js')
server.serve()
