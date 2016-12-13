import os, socket

sock = socket.create_connection(('127.0.0.1', 9300))
print(sock.send(b'x' * 65536))
sock.close()

from ctypes import *
libc = CDLL("libc.so.6")
get_errno_loc = libc.__errno_location
get_errno_loc.restype = POINTER(c_int)
print(get_errno_loc()[0])
print(os.strerror(get_errno_loc()[0]))
