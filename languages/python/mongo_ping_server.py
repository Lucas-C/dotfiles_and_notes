#!/usr/bin/env python3
# Reversed-engineered TCP server that can listen & answer to MongoDB "ping" requests like this:
#   echo 'db.runCommand("ping").ok' | mongo 127.0.0.1:27017 --verbose
# USAGE: ./mongodb_ping_server.py $host $port
# REQUIRE: pip install bson
from __future__ import print_function
import bson, socket, sys
from ctypes import *
from datetime import datetime
from itertools import count
from typing import Dict, NamedTuple
from socketserver import StreamRequestHandler, TCPServer


# Wire protocol doc: https://docs.mongodb.com/manual/reference/mongodb-wire-protocol/#standard-message-header
OP_REPLY = 1
OP_QUERY = 2004
OP_COMMAND = 2010
OP_COMMANDREPLY = 2011


class MongoMsgHeader(LittleEndianStructure):
    _fields_ = (
        ('messageLength', c_int),
        ('requestID', c_int),
        ('responseTo', c_int),
        ('opCode', c_int),
    )
    def asdict(self):
        return {k[0]:getattr(self, k[0]) for k in self._fields_}

class MongoOpQuery(NamedTuple):
    flags: int
    fullCollectionName: str
    numberToSkip: int
    numberToReturn: int
    query: Dict
    @classmethod
    def read_from_bytestream(cls, buffer_stream, messageLength):
        messageLength -= sizeof(MongoMsgHeader)
        flags = c_int.from_buffer_copy(buffer_stream.read(sizeof(c_int))).value             ;messageLength -= sizeof(c_int)
        fullCollectionName = read_cstring(buffer_stream)                                    ;messageLength -= len(fullCollectionName) + 1
        numberToSkip = c_int.from_buffer_copy(buffer_stream.read(sizeof(c_int))).value      ;messageLength -= sizeof(c_int)
        numberToReturn = c_int.from_buffer_copy(buffer_stream.read(sizeof(c_int))).value    ;messageLength -= sizeof(c_int)
        query = bson.loads(buffer_stream.read(messageLength))
        return cls(flags, fullCollectionName, numberToSkip, numberToReturn, query)

class MongoOpCommand(NamedTuple):
    database: str
    commandName: str
    metadata: Dict
    commandReply : Dict
    @classmethod
    def read_from_bytestream(cls, buffer_stream, messageLength):
        messageLength -= sizeof(MongoMsgHeader)
        database = read_cstring(buffer_stream)      ;messageLength -= len(database) + 1
        commandName = read_cstring(buffer_stream)   ;messageLength -= len(commandName) + 1
        buffer = buffer_stream.read(messageLength)
        metadata = bson.loads(buffer)
        commandReply = bson.loads(buffer[len(bson.dumps(metadata)):])
        return cls(database, commandName, metadata, commandReply)

def read_cstring(buffer):
    chars = b''
    while True:
        c = buffer.read(1)
        if c == b'\x00':
            return chars
        chars += c

class MongoOpReply(LittleEndianStructure):
    _pack_ = True
    _fields_ = (
        ('responseFlags', c_int),
        ('cursorID', c_long),
        ('startingFrom', c_int),
        ('numberReturned', c_int),
    )

def convert_struct_to_bytes(st):
    buffer = create_string_buffer(sizeof(st))
    memmove(buffer, addressof(st), sizeof(st))
    return buffer.raw

class RequestHandler(StreamRequestHandler):
    def handle(self):
        for i in count():  # infinite loop
            bytes_header = self.rfile.read(sizeof(MongoMsgHeader))
            if not bytes_header:
                break
            msg_header = MongoMsgHeader.from_buffer_copy(bytes_header)
            print('MSG_HEADER:', msg_header.asdict())
            {
                OP_QUERY: self._handle_op_query,
                OP_COMMAND: self._handle_op_command,
            }[msg_header.opCode](msg_header, msg_header.responseTo + i)

    def _handle_op_query(self, msg_header, responseTo):
        op_query = MongoOpQuery.read_from_bytestream(self.rfile, msg_header.messageLength)
        print('OP_QUERY:', dict(**op_query._asdict()))
        assert op_query.query['isMaster'] == 1
        op_reply = self._command_reply(b'isMaster')
        print('OP_REPLY:', op_reply)
        byteresp = convert_struct_to_bytes(MongoOpReply(responseFlags=8, cursorID=0, startingFrom=0, numberReturned=op_query.numberToReturn))
        byteresp += bson.dumps(op_reply)
        self._send_resp(OP_REPLY, byteresp, responseTo)

    def _handle_op_command(self, msg_header, responseTo):
        op_command = MongoOpCommand.read_from_bytestream(self.rfile, msg_header.messageLength)
        print('OP_COMMAND:', dict(**op_command._asdict()))
        cmd_reply = self._command_reply(op_command.commandName)
        print('OP_COMMANDREPLY:', cmd_reply)
        byteresp = bson.dumps(cmd_reply) + bson.dumps({})
        self._send_resp(OP_COMMANDREPLY, byteresp, responseTo)

    def _send_resp(self, op_code, byteresp, responseTo):
        msg_length = sizeof(MongoMsgHeader) + len(byteresp)
        self.wfile.write(convert_struct_to_bytes(MongoMsgHeader(messageLength=msg_length, requestID=0, responseTo=responseTo, opCode=op_code)) + byteresp)
        self.wfile.flush()

    def _command_reply(self, cmd_name):
        payloads = {
            b'whatsmyuri': {'you': ':'.join(map(str, self.connection.getpeername())), 'ok': 1.0},
            b'buildinfo': {'version': '3.4.4', 'gitVersion': '888390515874a9debd1b6c5d36559ca86b44babd', 'targetMinOS': 'Windows 7/Windows Server 2008 R2',
                           'modules': [], 'allocator': 'tcmalloc', 'javascriptEngine': 'mozjs', 'sysInfo': 'deprecated', 'versionArray': [3, 4, 4, 0],
                           'openssl': {'running': 'OpenSSL 1.0.1u-fips  22 Sep 2016', 'compiled': 'OpenSSL 1.0.1u-fips  22 Sep 2016'},
                           'buildEnvironment': {'distmod': '2008plus-ssl', 'distarch': 'x86_64', 'cc': 'cl: Microsoft (R) C/C++ Optimizing Compiler Version 19.00.24218.1 for x64',
                               'ccflags': '/nologo /EHsc /W3 /wd4355 /wd4800 /wd4267 /wd4244 /wd4290 /wd4068 /wd4351 /we4013 /we4099 /we4930 /Z7 /errorReport:none /MD /O2 /Oy- /bigobj /Gw /Gy /Zc:inline',
                               'cxx': 'cl: Microsoft (R) C/C++ Optimizing Compiler Version 19.00.24218.1 for x64',
                               'cxxflags': '/TP', 'linkflags': '/nologo /DEBUG /INCREMENTAL:NO /LARGEADDRESSAWARE /OPT:REF', 'target_arch': 'x86_64', 'target_os': 'windows'},
                           'bits': 64, 'debug': False, 'maxBsonObjectSize': 16777216, 'storageEngines': ['devnull', 'ephemeralForTest', 'mmapv1', 'wiredTiger'], 'ok': 1.0},
            b'isMaster': {'ismaster': True, 'maxBsonObjectSize': 16777216, 'maxMessageSizeBytes': 48000000, 'maxWriteBatchSize': 1000,
                          'localTime': datetime.utcnow(), 'maxWireVersion': 5, 'minWireVersion': 0, 'readOnly': False, 'ok': 1.0},
            b'replSetGetStatus': {'ok': 0.0, 'errmsg': 'not running with --replSet', 'code': 76, 'codeName': 'NoReplicationEnabled'},
        }
        payloads[b'buildInfo'] = payloads[b'buildinfo']
        return payloads[cmd_name]

TCPServer((sys.argv[1], int(sys.argv[2])), RequestHandler).serve_forever()
