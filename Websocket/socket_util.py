import base64
import hashlib

HOST = '127.1.1.0'
PORT = 50006
MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


def encode_socket(raw_data):
    data = bytes.hex(bytes(raw_data, 'utf-8'))
    lens = len(data) // 2

    len_str = len(hex(lens)[2:])

    if lens < 126:
        data = '0' * max(0, 2 - len_str) + hex(lens)[2:] + data
        # print(1, '0' * max(0, 2 - len_str) + hex(lens)[2:])
    elif lens < pow(2, 16) - 1:
        data = '7e' + '0' * max(0, 4 - len_str) + hex(lens)[2:] + data
        # print(2, '7e' + '0' * max(0, 4 - len_str) + hex(lens)[2:])
    else:
        data = '7f' + '0' * max(0, 16 - len_str) + hex(lens)[2:] + data
        # print(3, '7f' + '0' * max(0, 16 - len_str) + hex(lens)[2:])

    data = '81' + data

    return bytes.fromhex(data)


def decode_socket(raw_data):
    data = bin(int(bytes.hex(raw_data), 16))[2:]

    t = '0' + data[9:16]
    lens = int(t, 2)

    if lens == 126:
        pos = 2
    elif lens == 127:
        pos = 8
    else:
        pos = 0

    pos = (1 + 1 + pos) * 8
    data = data[pos:]

    xor = []
    for x in range(4):
        xor.append(int(data[x * 8: (x + 1) * 8], 2))

    data = data[4 * 8:]

    ans = ''
    for x in range(len(data) // 8):
        x = int(data[x * 8: x * 8 + 8], 2) ^ xor[x % 4]
        ans += '0' * max(0, 2 - len(str(hex(x))[2:])) + str(hex(x))[2:]

    return bytes.fromhex(ans).decode()


def trans(data):
    data += MAGIC_STRING
    return base64.b64encode(hashlib.sha1(data.encode()).digest())


def handle(data):
    for x in data.split('\r\n'):
        if x.split(':')[0] == 'Sec-WebSocket-Key':
            key = x.split(':')[1].strip()
    key = trans(key)
    rst = '''HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: {}

'''.format(key.decode(), HOST + ':' + str(PORT))
    return rst


def son_task(file_name, rpipe):
    out = open(file_name, 'a')
    f = open(rpipe)
    while True:
        data = f.readline()
        print('Son OK' + data)
        out.write(data)


if __name__ == '__main__':
    pass
