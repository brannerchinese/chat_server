#!/usr/bin/env python
# Rhodes and Goerzen, Foundations of Python Network Programming, tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets
# Converted to Python3 by David Branner, 20140703, works.

import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
PORT = 1060

def recv_all(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data)).decode('utf-8')
        if not more:
            raise EOFError('socket closed {} bytes into a {}-byte message'.
                    format(len(data), length))
        data += more
    return data

if sys.argv[1:] == ['server']:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        print('Listening at {}'.format(s.getsockname()))
        sc, sockname = s.accept()
        print('We have accepted a connection from {}'.
                format(sockname))
        print('Socket connects {} and {}.'.
                format(sc.getsockname(), sc.getpeername()))
        message = recv_all(sc, 16)
        print('The incoming sixteen-octet message says {}'.
                format(repr(message)))
        sc.sendall(b'Farewell, client')
        sc.close()
        print('Reply sent, socket closed')

elif sys.argv[1:] == ['client']:
    s.connect((HOST, PORT))
    print('Client has been assigned socket name {}'.format(s.getsockname()))
    s.sendall(b'Hi there, server')
    reply = recv_all(s, 16)
    print('The server said {}'.format(repr(reply)))
    s.close()

else:
    sys.stderr.write('usage: tcp_sixteen.py server|client [host]\n')

