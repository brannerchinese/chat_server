#! /usr/bin/env python3
# chat_three.py
# David Prager Branner
# 20140710

import socket
import sys
import random
import time

HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
PORT = 1060

def main():
    choices = {'server': run_server,
            'client': run_client,
            }
    choice = ''
    if 1 < len(sys.argv) < 3:
        choice = sys.argv[1:][0]
    if choice in choices:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                choices[choice](s)
            except ConnectionRefusedError:
                print('Connection refused.')
            except ConnectionResetError:
                print('Connection reset.')
            s.close()
    else:
        sys.stderr.write('''Received argument {}\n'''
                '''Usage: chat_three.py server|client [host]\n'''.
                format(choice))

def recv_full_msg(sock):
    message = ''
    more = ''
    while '\n' not in more:
        more = str(sock.recv(16), 'utf-8')
        message += more
    return message.strip('\n')

def run_server(s):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print('Listening at {}'.format(s.getsockname()))
    clients = set([None])
    while clients:
        print(clients)
        clients.remove(None)
        clients.add(s.accept()) # sc, sockname
        print(clients)
        to_remove = set()
        for sc, sockname in list(clients):
            print('We have accepted a connection from {}'.
                    format(sockname))
            print('Socket connects {} and {}.'.
                    format(sc.getsockname(), sc.getpeername()))
            while True:
                message = recv_full_msg(sc)
                if message in ['bye', '', None]:
                    # Remember to remove this client from clients
                    to_remove.add((sc, sockname))
                    sc.sendall(b'Farewell, client\n')
                    sc.close()
                    print('Reply sent to {}, socket closed'.
                            format(sockname))
                    break
                print('The incoming message says {}'.format(message))
                sc.sendall(bytes(message + '\n', 'utf-8'))
        clients = clients - to_remove
        print('after removal:', clients)
    s.close()

def run_client(s):
    s.connect((HOST, PORT))
    print('Client has been assigned socket name {}'.format(s.getsockname()))
    while True:
        message = input(': ')
        if not message:
            continue
        else:
            message += '\n'
        s.sendall(bytes(message, 'utf-8'))
        reply = recv_full_msg(s)
        print('The server said {}'.format(str(reply)))
        if message == 'bye\n':
            break

if __name__ == '__main__':
    main()