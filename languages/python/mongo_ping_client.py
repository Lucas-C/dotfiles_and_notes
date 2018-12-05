#!/usr/bin/env python3

# Zero-dependency, minimal TCP client to check if it is possible to communicate with a MongoDB server,
# without installing the MongoDB shell or any client

# USAGE: ./mongo_ping_client.py $host $port [$payload_index]

from __future__ import print_function
import socket, sys
from ctypes import c_int

PAYLOADS = (
    # OP_QUERY: {'flags': 0, 'fullCollectionName': b'admin.$cmd', 'numberToSkip': 0, 'numberToReturn': 1, 'query': {'isMaster': 1, 'client': {'application': {'name': 'MongoDB Shell'}, 'driver': {'name': 'MongoDB Internal Client', 'version': '3.4.4'}, 'os': {'type': 'Windows'$ 'name': 'Microsoft Windows 8', 'architecture': 'x86_64', 'version': '6.2 (build 9200)'}}}}
    b'#\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd4\x07\x00\x00\x00\x00\x00\x00admin.$cmd\x00\x00\x00\x00\x00\x01\x00\x00\x00\xfc\x00\x00\x00\x10isMaster\x00\x01\x00\x00\x00\x03client\x00\xe1\x00\x00\x00\x03application\x00\x1d\x00\x00\x00\x02name\x00\x0e\x00\x00\x00MongoDB Shell\x00\x00\x03driver\x00:\x00\x00\x00\x02name\x00\x18\x00\x00\x00MongoDB Internal Client\x00\x02version\x00\x06\x00\x00\x003.4.4\x00\x00\x03os\x00l\x00\x00\x00\x02type\x00\x08\x00\x00\x00Windows\x00\x02name\x00\x14\x00\x00\x00Microsoft Windows 8\x00\x02architecture\x00\x07\x00\x00\x00x86_64\x00\x02version\x00\x11\x00\x00\x006.2 (build 9200)\x00\x00\x00\x00',
    # OP_COMMAND: {'database': b'admin', 'commandName': b'whatsmyuri', 'metadata': {'whatsmyuri': 1}, 'commandReply': {}}
    b';\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00admin\x00whatsmyuri\x00\x15\x00\x00\x00\x10whatsmyuri\x00\x01\x00\x00\x00\x00\x05\x00\x00\x00\x00',
    # OP_COMMAND: {'database': b'admin', 'commandName': b'buildinfo', 'metadata': {'buildinfo': 1.0}, 'commandReply': {}}
    b'=\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00admin\x00buildinfo\x00\x18\x00\x00\x00\x01buildinfo\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x05\x00\x00\x00\x00',
    # OP_COMMAND: {'database': b'test', 'commandName': b'isMaster', 'metadata': {'isMaster': 1.0, 'forShell': 1.0}, 'commandReply': {}}
    b'L\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00test\x00isMaster\x00)\x00\x00\x00\x01isMaster\x00\x00\x00\x00\x00\x00\x00\xf0?\x01forShell\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x05\x00\x00\x00\x00',
    # OP_COMMAND: {'database': b'admin', 'commandName': b'replSetGetStatus', 'metadata': {'replSetGetStatus': 1.0, 'forShell': 1.0}, 'commandReply': {}}
    b']\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\xda\x07\x00\x00admin\x00replSetGetStatus\x001\x00\x00\x00\x01replSetGetStatus\x00\x00\x00\x00\x00\x00\x00\xf0?\x01forShell\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x05\x00\x00\x00\x00',
)

tcp_connection = socket.create_connection((sys.argv[1], int(sys.argv[2])))
payload_index = int(sys.argv[3]) if len(sys.argv) > 3 else 1
data = PAYLOADS[payload_index]
tcp_connection.sendall(data)
msg_header = tcp_connection.recv(16)
messageLength = c_int.from_buffer_copy(msg_header[:4]).value
resp = tcp_connection.recv(messageLength - 16)
print('SUCCESS!')
try:
    import bson
    doc = resp[20:] if payload_index == 0 else resp
    print(bson.loads(doc))
except ImportError:
    print(resp)
