#! /usr/bin/env python
# client.py
# David Prager Branner
# 20140711

"""Create and run client for AsyncIO server."""

import asyncio
import sys
import os
import random

clients = {}  # task -> (reader, writer)


def make_connection(host, port):
    task = asyncio.Task(handle_client(host, port))

@asyncio.coroutine
def handle_client(host, port):
    print("Connecting to {} {}".format(host, port))
    try:
        streamreader, streamwriter = (
                yield from asyncio.open_connection(host, port))
    except OSError: # first: ConnectionRefusedError
        sys.exit('Exception')
    try:
        # Prepare for client log-in.
        data = yield from asyncio.wait_for(
                streamreader.readline(), timeout=None)
        data = data.decode().rstrip()
        if data != 'Connection made.':
            streamwriter.write('Expected "Connection made." Received "{}"'.
                    format(data))
            return
        else:
            print("Connected to {} {}".format(host, port))
        #
        # Instructions.
        print('''A colon (:) at the beginning of a line is a prompt; enter '''
                '''your message after it and submit with carriage-return.''')
        print('Disconnect using "q" alone on a line.")
        #
        # Log in.
        login = input('login: ')
        streamwriter.write((login + '\n').encode())
        #
        # Prepare for messages
        data = yield from asyncio.wait_for(
                streamreader.readline(), timeout=None)
        data = data.decode().rstrip()
        if data != 'ready for messages':
            print('Expected "ready for messages", received "{}"'.format(data))
            return
        #
        # Message loop.
        while True:
            message = input(': ')
            if not message:
                continue
            if message.lower() == 'q':
                streamwriter.write('q\n'.encode())
                # Confirm quit.
                data = yield from asyncio.wait_for(
                        streamreader.readline(), timeout=None)
                if data.decode().rstrip() == 'q':
                    break
            # send each string and get a reply, it should be an echo back
            streamwriter.write(('{}\n'.format(message)).encode())
            data = yield from asyncio.wait_for(
                    streamreader.readline(), timeout=None)
            data = data.decode().rstrip()
            print(data)
    except KeyboardInterrupt: # Treat like regular quit.
        streamwriter.write('q\n'.encode())
    except ConnectionResetError: # If server is down.
        print('Connection reset; server not found.')
    finally:
        print("\nDisconnecting from {} {}".format(host, port))
        streamwriter.close()
        print("Disconnected from {} {}".format(host, port))
        os._exit(1) # Quit cleanly.

def whether_to_quit(streamreader, streamwriter):
    # Quit.
    streamwriter.write('q\n'.encode())
    # Confirm quit.
    data = yield from asyncio.wait_for(
            streamreader.readline(), timeout=None)
    return data.decode().rstrip() == 'q'

def main():
    # Choose port.
    if len(sys.argv) < 2:
        sys.argv.append(137)
    random.seed(sys.argv[1])
    PORT = random.randint(49152, 65535)
    # Start loop.
    loop = asyncio.get_event_loop()
    make_connection('localhost', PORT)
    loop.run_forever()

if __name__ == '__main__':
    main()
