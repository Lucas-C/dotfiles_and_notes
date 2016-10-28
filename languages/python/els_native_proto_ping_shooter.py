import os, socket
try:
    sock = socket.create_connection(('127.0.0.1', 9300))
    sent_bytes_count = sock.send(b'ES\xFF\xFF\xFF\xFF')  # cf. https://github.com/elastic/elasticsearch/blob/v2.4.0/core/src/main/java/org/elasticsearch/transport/netty/NettyTransport.java#L1326 / https://github.com/elastic/elasticsearch/blob/master/core/src/main/java/org/elasticsearch/transport/TcpTransport.java#L244
    if sent_bytes_count == 6:
        print('ping OK')
    else:
        assert sent_bytes_count is None  # cf. https://github.com/python/cpython/blob/master/Modules/socketmodule.c#L3721
        print('ping KO (send failed: errno should indicate why)')  # cf. https://linux.die.net/man/2/send & http://stackoverflow.com/questions/661017/access-to-errno-from-python
        # How to test this code branch ?
        from ctypes import CDLL, POINTER, c_int
        get_errno_loc = CDLL("libc.so.6").__errno_location
        get_errno_loc.restype = POINTER(c_int)
        print(os.strerror(get_errno_loc()[0]))
    sock.close()
except ConnectionRefusedError:
    print('ping KO (ConnectionRefused)')
