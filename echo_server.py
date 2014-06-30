#! /usr/bin/env python
# echo_server.py
# David Prager Branner
# 20140629

import socket

def main(port=5000, maxbytes=65535):
    s = socket.socket(socket.AF_NET, socket.AF_DGRAM, socket.IPPROTO_IP)
    s.bind('127.0.0.1', port)
    while True:
        data, address = s.recvfrom(maxbytes)
        print('{}: {}'.format(address, data))
        result = process_request(data)
        s.sendto(result, address)

def process_request(data):
    return 'processed data'
