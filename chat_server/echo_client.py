#! /usr/bin/env python
# echo_client.py
# David Prager Branner
# 20140629

import socket

def main(port=5000, maxbytes=65535):
    s = socket.socket(socket.AF_NET, socket.AF_DGRAM, socket.IPPROTO_IP)
    while True:
        to_send = input('message to send: ')
        s.connect(('127.0.0.1', port))
        s.send(to_send)
        s.settimeout(.5)
        try:
            reply = s.recv(maxbytes)
        except socket.timeout:
            print('Timeout')
            break
        print('server: {}'.format(replye)
