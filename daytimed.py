#!/usr/bin/python

import os
import socket
import syslog
import time

from socketserver import (
    BaseRequestHandler,
    UDPServer,
    TCPServer
)


class DaytimeUDPHandler(BaseRequestHandler):
    protocol = 'udp'

    class cache:
        second = 0
        daytime = b''

    def handle(self):
        data, sock = self.request
        sock.sendto(self.daytime(), self.client_address)
        self.client_msg = data

    def finish(self) -> None:
        syslog.syslog(
            syslog.LOG_INFO,
            '{} {}:{} send {}, recv {}'.format(
                self.protocol,
                *self.client_address[:2],
                self.cache.daytime,
                self.client_msg
            )
        )

    def daytime(self):
        second = int(time.time())
        cache = self.cache
        if cache.second != second:
            cache.second = second
            cache.daytime = time.strftime('%a %F %T %Z\n').encode('ascii')
        return cache.daytime


class DaytimeTCPHandler(DaytimeUDPHandler):
    protocol = 'tcp'

    def handle(self):
        self.request.send(self.daytime())
        self.request.settimeout(0)
        try:
            self.client_msg = self.request.recv(1024)
        except:
            self.client_msg = b''


class IPv6TCPServer(TCPServer):
    address_family = socket.AF_INET6


class IPv6UDPServer(UDPServer):
    address_family = socket.AF_INET6


if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        server = IPv6TCPServer(('', 13), DaytimeTCPHandler)
        server.serve_forever()
    else:
        server = IPv6UDPServer(('', 13), DaytimeUDPHandler)
        server.serve_forever()
