#!/usr/bin/python

import socket
import sys


def error(msg, *args):
    print('daytime:', msg, *args, file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        error('Server address is need')
        sys.exit(2)

    server_address = sys.argv[1]
    family = socket.AF_INET6 if ':' in server_address else socket.AF_INET
    client_socket = socket.socket(family, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)

    try:
        client_socket.sendto(b'daytime.py', (server_address, 13))
        data, _ = client_socket.recvfrom(1024)
        date = data.decode().strip()
        print(date)
    except:
        error('Failed to get daytime from', server_address)
        sys.exit(1)


if __name__ == '__main__':
    main()
