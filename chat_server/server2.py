#! /usr/bin/env python
# server1.py
# Based on https://gist.github.com/dbehnke/9627160
# 20140712, does not work

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
        print('Log-in by {}'.format(login))
        # Store log-in: client in dictionary.
        clients_by_login[login] = (streamreader, streamwriter)
    # Let client know server is ready for messages.
    streamwriter.write("ready for messages\n".encode())
    #
    # Begin message loop
    while True:
        # wait for input from client
        message = yield from asyncio.wait_for(
                streamreader.readline(), timeout=None)
        if message is None:
            print("Received no data")
            continue
        message = message.decode().rstrip()
        if message.lower() == 'q':
            streamwriter.write("q\n".encode())
            break
        # See if the message contains a destination.
        elif message.find(':'):
            # ':' is present; see if left side is username(s).
            try:
                users, message = message.split(':', 1)
                print('Got user(s): {}; message: {}'.format(users, message))
                # Look up all users.
                users = [user.strip() for user in users.split(',')]
                if all([user in clients_by_login for user in users]):
                # Send message to all users, prefixed by sender.
                    for user in users:
                        print('''message for {}\n        from {}'''.
                                format(clients_by_login[user][1], 
                                clients_by_login[login][1]))
                        print('Current users are {}'.format(
                                [clients_by_login[i][1]
                                for i in clients_by_login]))
                        clients_by_login[user][1].write(
                                (login + ': ' + message + '\n').encode())
            except ValueError:
                print('Got indivisible message: {}'.format(message))
                # We assume the server is being tested.
                # Echo string back to sender.
                response = ("you sent: {}\n".format(message))
                try:
                    streamwriter.write(response.encode())
                except OSError:
                    print('Exception')
                    break

def main():
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
