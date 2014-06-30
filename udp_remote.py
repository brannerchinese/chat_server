#! /usr/bin/env python
# Rhodes and Goerzen, Foundations of Python Network Programming, udp_remote.py
# UDP client and server for talking over the network
# Converted to Python3 by David Branner, 20140629

import random, socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 53565
PORT = 1060

if 2 <= len(sys.argv) <= 3 and sys.argv[1] == 'server':
    interface = sys.argv[2] if len(sys.argv) > 2 else ''
    s.bind((interface, PORT))
    print('listening at {}'.format(s.getsockname()))
    while True:
        data, address = s.recvfrom(MAX)
        if random.randint(0, 1):
            print('The client at {} says {}'.
                    format(address, data.decode('utf-8')))
            s.sendto(bytes('Your data was {} bytes.'.format(len(data)),
                'utf-8'), address)
        else:
            print('Pretending to drop packet from {}.'.format(address))

elif len(sys.argv) == 3 and sys.argv[1] == 'client':
    hostname = sys.argv[2]
    s.connect((hostname, PORT))
    print('Client socket name is {}.'.format(s.getsockname()))
    delay = 0.1
    while True:
        s.send(b'This is another message')
        print('Waiting up to {} seconds for a reply'.format(delay))
        s.settimeout(delay)
        try:
            data = s.recv(MAX)
        except socket.timeout:
            delay *= 2 # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down')
            continue
        except:
            raise # a real error, so we let the user see it
            continue
        else:
            break # we are done, and can stop looping
    print('The server says: {}'.format(data.decode('utf-8')))
else:
    print('usage: udp_remote.py server [ <interface> ]',
            file=sys.stderr)
    print(' or: udp_remote.py client <host>', file=sys.stderr)
    sys.exit(2)
