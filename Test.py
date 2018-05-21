import os
import time


def son(w):
    f = open(w)
    out = open('news.txt', 'w')
    while True:
        recv = f.readline()
        print(recv + ' OK')
        out.write(recv)


if __name__ == '__main__':
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        son(r)
        exit(0)

    while True:
        data = input() + '\n'
        os.write(w, data.encode())
