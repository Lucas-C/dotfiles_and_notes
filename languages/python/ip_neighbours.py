#!/usr/bin/env python3

# Find closest IP around the given one,
# answer on the given ports (default: 80 & 443)

import socket, sys
from urllib.request import urlopen


def main(ip, ports):
    if not ip:
        # Same as: dig +short myip.opendns.com @resolver1.opendns.com
        with urlopen('https://api.ipify.org') as response:
            ip = response.read().decode()
        print('IP not provided, using this machine public IP:', ip)
    ip = list(map(int, ip.split('.')))
    for last_byte in range(0, ip[3]):
        test_ip = '.'.join(map(str, ip[:3] + [last_byte]))
        if _test_connection_to_ip_and_print('LEFT:', test_ip, ports):
            break
    for last_byte in range(ip[3]+1, 256):
        test_ip = '.'.join(map(str, ip[:3] + [last_byte]))
        if _test_connection_to_ip_and_print('RIGHT:', test_ip, ports):
            break

def _test_connection_to_ip_and_print(prefix, ip, ports):
    for port in ports:
        try:
            socket.create_connection((ip, port))
            print(prefix, ip, port)
            return True
        except (ConnectionRefusedError, TimeoutError):
            pass


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None, (80, 443))
