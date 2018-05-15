from socket_util import *


class websocket:
    BUFFER_SIZE = 65536

    def __init__(self, s, addr):
        self.s = s
        self.addr = addr
        self.hello()

    def hello(self):
        data = self.s.recv(self.BUFFER_SIZE).decode()
        data = bytes(handle(data).replace('\n', '\r\n'), 'utf-8')
        self.s.sendall(data)

    def send(self, data):
        self.s.sendall(encode_socket(data))

    def receive(self):
        data = self.s.recv(self.BUFFER_SIZE)
        if not data or data[0] == 136:
            return None
        return decode_socket(data)
