import socket
import threading
import os
import json
from websocket import websocket
from socket_util import *

DATA_NAME = 'news.txt'


class server:
    def __init__(self, host='127.0.0.1', port=50006):
        self.users = []
        self.news = []
        self.s = socket.socket()
        self.s.bind((host, port))
        self.s.listen(5)
        self.names = []

        data = open(DATA_NAME)
        for item in data.read().split('\n'):
            if len(item) == 0:
                continue
            self.news.append(item)

        rpipe, wpipe = os.pipe()
        pid = os.fork()
        if pid == 0:
            os.close(wpipe)
            son_task(DATA_NAME, rpipe)
            exit(0)
        os.close(rpipe)
        self.wpipe = wpipe

    def send_to_all(self, data):
        for s in self.users:
            s.send(data)

    def save_news(self, data):
        os.write(self.wpipe, (data + '\n').encode())

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
                # print(data)
                tmp = json.loads(data)
                name = tmp.get('username')
                if name and self.names.count(name) == 0:
                    self.names.append(name)
                self.send_to_all(data)
                if tmp.get('type') == 'message':
                    self.news.append(data)
                    self.save_news(data)
            except Exception:
                pass

        if name:
            data = {'type': 'del_user', 'username': name}
            self.send_to_all(json.dumps(data))
            self.names.remove(name)
        print('Disconnect', c.addr[1])
        self.users.remove(c)

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


if __name__ == '__main__':
    s = server()
    s.run()
