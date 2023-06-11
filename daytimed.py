#!/usr/bin/python

import time
import syslog
import os

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
        _, sock = self.request
        sock.sendto(self.daytime(), self.client_address)

    def finish(self) -> None:
        syslog.syslog(
            syslog.LOG_INFO,
            'replied {} client {}:{}'.format(
                self.protocol,
                *self.client_address
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


if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        server = TCPServer(('', 13), DaytimeTCPHandler)
        server.serve_forever()
    else:
        server = UDPServer(('', 13), DaytimeUDPHandler)
        server.serve_forever()
