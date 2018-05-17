import socket
import threading
import json
from websocket import websocket
from socket_util import *


class server:
    def __init__(self, host='127.0.0.1', port=50006):
        self.users = []
        self.news = []
        self.s = socket.socket()
        self.s.bind((host, port))
        self.s.listen(5)
        self.names = []

    def run(self):
        while True:
            conn, addr = self.s.accept()
            try:
                c = websocket(conn, addr)
                print('Connected by', addr[1])
                self.users.append(c)
                threading.Thread(target=self.process, args=((c,))).start()
            except Exception:
                pass

    def send_to_all(self, data):
        for s in self.users:
            s.send(data)

    def process(self, c):
        for info in self.news:
            c.send(info)
        for name in self.names:
            data = {'type': 'add_user', 'username': name}
            c.send(json.dumps(data))

        name = None

        while True:
            try:
                data = c.receive()
                if not data:
                    break
                print(data)
                tmp = json.loads(data)
                name = tmp.get('username')
                if name and self.names.count(name) == 0:
                    self.names.append(name)
                self.send_to_all(data)
                if tmp.get('type') == 'message':
                    self.news.append(data)
            except Exception:
                pass

        if name:
            data = {'type': 'del_user', 'username': name}
            self.send_to_all(json.dumps(data))
            self.names.remove(name)
        print('Disconnect', c.addr[1])
        self.users.remove(c)


if __name__ == '__main__':
    s = server()
    s.run()
