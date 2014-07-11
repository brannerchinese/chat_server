#! /usr/bin/env python3
# chat_server.py
# Sending data one block at a time.

import socket
import sys
import random
import time

HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
SERVER_PORT = 1060

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    choices = {'server': run_server,
            'client': run_client,
            }
    choice = sys.argv[1:][0]
    if choice in choices:
        choices[choice](s)
    else:
        sys.stderr.write('''Received argument {}\n'''
                '''Usage: streamer.py server|client [host]\n'''.
                format(choice))

def get_message(sc, to_confirm=None):
    """Retrieve \n-delimited message; return it or confirmation boolean."""
    message = ''
    while True:
        more = sc.recv(8192) # arbitrary value of 8k
        if b'\n' in more: # message ends
            break
        message += str(more, 'utf-8')
    if to_confirm == None:
        return message
    else:
        return message == to_confirm

def run_client(s):
    s.connect((HOST, SERVER_PORT))
    # Ask for a dedicated port and open socket connection there.
    while True:
        s.sendall(b'assign socket')
        time.sleep(2)
#    s.listen(5)
    sc, sockname = s.recv(8192)
    s.close()
    print(sc, sockname)
    return
    sc.connect(sockname)
    while True:
        message = input(': ')
        # Identify recipient of message.
        
        # Send message.
        try:
            sc.sendall(bytes(message + '\n', 'utf-8'))
        except KeyboardInterrupt:
            break
        finally:
            # Get confirmation of message.
            if not get_message(sc, message):
                print('message not confirmed')
    sc.shutdown(socket.SHUT_RD)
    sc.close()

def run_server(s):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, SERVER_PORT))
    s.listen(5)
    print('Listening at {}'.format(s.getsockname()))
    sc, sockname = s.accept()
    print('Accepted connection from {}'.format(sockname))
    sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sc.bind(sockname)
    sc.listen(1)
    while True:
        message = get_message(sc)
        if message == 'assign socket':
            print('Message received for server:\n{}'.format(message))
            port = get_open_port(s)
            print(port)
            break
            sc.sendall(bytes(port + '\n', 'utf-8'))
            break
        else:
            print(message)
            break
    sc.shutdown(socket.SHUT_WR)
    sc.close()
    s.close()

def get_open_port(s):
    while True:
        try_port = random.randint(49152, 65535)
        try:
            s.bind((HOST, try_port))
            break
        except OSError:
            pass
    return try_port

if __name__ == '__main__':
    main()