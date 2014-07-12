# client.py
# Based on https://gist.github.com/dbehnke/9627160
# 20140711

"""Create client for AsyncIO server."""

import asyncio
import sys

clients = {}  # task -> (reader, writer)


def make_connection(host, port):
    task = asyncio.Task(handle_client(host, port))
#    clients[task] = (host, port)
#    def client_done(task):
#        del clients[task]
#        print("Client Task Finished")
#        if len(clients) == 0:
#            print("clients is empty, stopping loop.")
#            loop = asyncio.get_event_loop()
#            loop.stop()
#    print("New Client Task")
#    task.add_done_callback(client_done)


@asyncio.coroutine
def handle_client(host, port):
    print("Connecting to {} {}".format(host, port))
    try:
        client_reader, client_writer = (
                yield from asyncio.open_connection(host, port))
    except OSError: # first: ConnectionRefusedError
        sys.exit('Exception')
    try:
        # Prepare for client log-in.
        data = yield from asyncio.wait_for(
                client_reader.readline(), timeout=None)
        sdata = data.decode().rstrip()
        if sdata != 'Connection made.':
            client_writer.write('Expected "Connection made." Received "{}"'.
                    format(sdata))
            return
        else:
            print("Connected to {} {}".format(host, port))
        #
        # Log in.
        login = input('login: ')
        client_writer.write((login + '\n').encode())
        #
        # Prepare for messages
        data = yield from asyncio.wait_for(
                client_reader.readline(), timeout=None)
        sdata = data.decode().rstrip()
        if sdata != 'ready for messages':
            print('Expected "ready for messages", received "{}"'.format(sdata))
            return
        #
        # Message loop.
        while True:
            message = input(': ')
            if not message:
                continue
            if message.lower() == 'bye':
                break
            # send each string and get a reply, it should be an echo back
            client_writer.write(('{}\n'.format(message)).encode())
            data = yield from asyncio.wait_for(
                    client_reader.readline(), timeout=None)
            sdata = data.decode().rstrip()
            print(sdata)

        # send BYE to disconnect gracefully
        client_writer.write('bye\n'.encode())
        # receive BYE confirmation
        data = yield from asyncio.wait_for(
                client_reader.readline(), timeout=None)

        sdata = data.decode().rstrip().upper()
        print("Received '%s'" % sdata)
    except ConnectionResetError:
        print('Connection reset; exiting.')
    finally:
        print("Disconnecting from {} {}".format(host, port))
        client_writer.close()
        print("Disconnected from {} {}".format(host, port))


def main():
    loop = asyncio.get_event_loop()
    make_connection('localhost', 2991)
    try:
        loop.run_forever()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
