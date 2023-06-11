#!/usr/bin/python

import socket
import sys


def error(msg, *args):
    print('daytime:', msg, *args, file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        error('Server address is need')
        sys.exit(2)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    server_address = sys.argv[1]

    try:
        client_socket.sendto(b'What time is it now?', (server_address, 13))
        data, _ = client_socket.recvfrom(1024)
        date = data.decode().strip()
        print(date)
    except:
        error('Failed to get daytime from', server_address)
        sys.exit(1)


if __name__ == '__main__':
    main()
