#! /usr/bin/env python
# server.py
# David Prager Branner
# 20140711

"""Launch and run AsyncIO Server."""

import asyncio
import random
import sys
import os

clients = {}           # task:  (reader, writer); for control of tasks
clients_by_login = {}  # login: (reader, writer); for sending messages

def accept_client(streamreader, streamwriter):
    """Accept client and delete when finished."""
    task = asyncio.Task(handle_client(streamreader, streamwriter))
    clients[task] = (streamreader, streamwriter)
    def client_done(task):
        """Delete client."""
        del clients[task]
        streamwriter.close()
        print('End connection; {}'.format(count_connections()))
    print('New connection made; {}'.format(count_connections()))
    task.add_done_callback(client_done)

def count_connections():
    """Report the number of active clients."""
    number_clients = len(clients)
    if number_clients == 1:
        quote = 'is now 1 connection'
    else:
        quote = 'are now {} connections'.format(number_clients)
    return 'there {}.'.format(quote)

@asyncio.coroutine
def handle_client(streamreader, streamwriter):
    # Begin client log-in: 
    #   establish connection and add login to clients_by_login.
    streamwriter.write("Connection made.\n".encode())
    login = ''
    while not login:
        try:
            data = yield from asyncio.wait_for(
                    streamreader.readline(), timeout=None)
        except OSError:
            print('Exception')
            break
        if data is None:
            continue
        login = data.decode().rstrip()
        print('Log-in by user "{}"'.format(login))
        # Store log-in: client in dictionary.
        clients_by_login[login] = (streamreader, streamwriter)
    # now be an echo back server until client sends a bye
    # let client know we are ready
    streamwriter.write("ready for messages\n".encode())
    while True:
        # wait for input from client
        data = yield from asyncio.wait_for(
                streamreader.readline(), timeout=None)
        if data is None:
            print("Received no data")
            return
        data = data.decode().rstrip()
        if data.lower() == 'q':
            streamwriter.write("q\n".encode())
            break
        response = ("Confirming your message: {}\n".format(data))
        try:
            streamwriter.write(response.encode())
        except OSError:
            print('Exception')
            break

def main():
    print('''To quit, use control-c.''')
    # Choose port.
    if len(sys.argv) < 2:
        sys.argv.append(137)
    random.seed(sys.argv[1])
    PORT = random.randint(49152, 65535)
    # Start loop.
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=PORT)
    loop.run_until_complete(f)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()

if __name__ == '__main__':
    main()
