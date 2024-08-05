#!/usr/bin/env python3
# Script Dependencies:
#    livereload
import webbrowser
from livereload import Server

server = Server()
server.watch('index.html')
webbrowser.open('http://localhost:5500')
server.serve()
