# client.py
# Based on https://gist.github.com/dbehnke/9627160
# 20140711

"""Create client for AsyncIO server."""

import asyncio
import sys
import os

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
        streamreader, streamwriter = (
                yield from asyncio.open_connection(host, port))
    except OSError: # first: ConnectionRefusedError
        sys.exit('Exception')
    try:
        # Prepare for client log-in.
        data = yield from asyncio.wait_for(
                streamreader.readline(), timeout=None)
        sdata = data.decode().rstrip()
        if sdata != 'Connection made.':
            streamwriter.write('Expected "Connection made." Received "{}"'.
                    format(sdata))
            return
        else:
            print("Connected to {} {}".format(host, port))
        #
        # Log in.
        login = input('login: ')
        streamwriter.write((login + '\n').encode())
        #
        # Prepare for messages
        data = yield from asyncio.wait_for(
                streamreader.readline(), timeout=None)
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
            if message.lower() == 'q':
                if whether_to_quit(streamreader, streamwriter) == 'q':
                    break
            # send each string and get a reply, it should be an echo back
            streamwriter.write(('{}\n'.format(message)).encode())
            data = yield from asyncio.wait_for(
                    streamreader.readline(), timeout=None)
            sdata = data.decode().rstrip()
            print(sdata)
    except KeyboardInterrupt:
        streamwriter.write('q\n'.encode())
    except ConnectionResetError:
        print('Connection reset; server not found.')
    finally:
        print("\nDisconnecting from {} {}".format(host, port))
        streamwriter.close()
        print("Disconnected from {} {}".format(host, port))
        os._exit(1)

def whether_to_quit(streamreader, streamwriter):
    # Quit.
    streamwriter.write('q\n'.encode())
    # Confirm quit.
    data = yield from asyncio.wait_for(
            streamreader.readline(), timeout=None)
    return data.decode().rstrip()


def main():
    loop = asyncio.get_event_loop()
    make_connection('localhost', 2991)
    loop.run_forever()

if __name__ == '__main__':
    main()
