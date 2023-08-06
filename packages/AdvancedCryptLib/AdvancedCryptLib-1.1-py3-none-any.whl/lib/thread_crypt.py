import socket
import os
import sys

from cryptlib.random_generator import RandomGenerator


def crypt(message: bytes, generator: RandomGenerator):
    c = bytearray()
    for b in message:
        c.append(b ^ generator.next()[0])

    return bytes(c)


def get_key():
    k = input('Enter key: ')
    key = bytes([int(k[i] + k[i + 1], 16) for i in range(0, len(k), 2)])
    return key


def write_key(keyfile, key):
    k = ''.join((hex(i)[2:].zfill(2) for i in key))
    keyfile.write(k + '\n')


mode = input('Enter mode: \n\t[0] - server mode,\n\t[1] - client mode.\n\tMode ==== [0]> ')
if not mode:
    mode = '0'

if mode == '0':
    print_key = input('[p]rint key to console or write to [f]ile? ')
    key = os.urandom(256)
    keyfile = sys.stdout if print_key == 'p' else open('../key.txt', 'w')
    write_key(keyfile, key)
    if keyfile.name != '<stdout>':
        keyfile.close()
    s = socket.socket()
    s.bind(('0.0.0.0', 12345))
    s.listen(1)
    conn, addr = s.accept()
else:
    addr = input('Type server address [localhost]> ')
    if not addr:
        addr = 'localhost'

    key = get_key()
    conn = socket.socket()
    conn.connect((addr, 12345))

generator = RandomGenerator(key)

if mode == '0':
    conn.send(crypt(b'Hello, world!'.zfill(1024), generator))
raw_data = conn.recv(1024)
data = crypt(raw_data, generator)
if mode == '1':
    conn.send(crypt(b'Hello, world!'.zfill(1024), generator))

print(raw_data.decode(errors='ignore'))

if data.decode().lstrip('0') != 'Hello, world!':
    print('Error!')