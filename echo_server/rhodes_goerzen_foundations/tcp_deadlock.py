#!/usr/bin/env python
# Rhodes and Goerzen, Foundations of Python Network Programming, tcp_deadlock.py
# TCP client and server that leave too much data waiting
# Converted to Python3 by David Branner, 20140703

import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 1060

if sys.argv[1:] == ['server']:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        print('Listening at {}'.format(s.getsockname()))
        sc, sockname = s.accept()
        print('Processing up to 1024 bytes at a time from {}'.
                format(sockname))
        n = 0
        while True:
            message = sc.recv(1024).decode('utf-8')
            if not message:
                break
            sc.sendall(message.upper().encode())
            n += len(message)
            print('{} bytes processed so far.'.format(n))
            sys.stdout.flush()
            print()
        sc.close()
        print('Completed processing.')

elif len(sys.argv) == 3 and sys.argv[1] == 'client' and sys.argv[2].isdigit():
    bytes = (int(sys.argv[2]) + 15) // 16 * 16 # round up to // 16
    message = b'capitalize this!' # 16-byte message to repeat over and over
    print('Sending {} byles of data, in chunks of 16 bytes.'.format(bytes))
    s.connect((HOST, PORT))
    sent = 0
    while sent < bytes:
        s.sendall(message)
        sent += len(message)
        print('\r{} bytes sent.'.format(sent))
        sys.stdout.flush()
    print()
    s.shutdown(socket.SHUT_WR)
    print('Receiving all the data the server sends back.')
    received = 0
    while True:
        data = s.recv(42)
        if not received:
            print('The first data received says {}.'.
                    format(data.decode('utf-8')))
        received += len(data)
        if not data:
            break
        print('\r{} bytes received.'.format(received))
    s.close()

else:
    sys.stderr.write('usage: tcp_deadlock.py server|client <bytes>\n')


