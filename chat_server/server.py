# server.py
# Based on https://gist.github.com/dbehnke/9627160
# 20140711

"""Launch AsyncIO Server"""

import asyncio

clients = {}           # task:  (reader, writer)
clients_by_login = {}  # login: (reader, writer)

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
    login = ''
    while not login:
        streamwriter.write("Connection made.\n".encode())
        data = yield from asyncio.wait_for(
                streamreader.readline(), timeout=None)
        if data is None:
            continue
        login = data.decode().rstrip()
        print('Log-in by {}'.format(login))
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
        sdata = data.decode().rstrip()
        if sdata.lower() == 'q':
            streamwriter.write("q\n".encode())
            break
        response = ("you sent: {}\n".format(sdata))
        try:
            streamwriter.write(response.encode())
        except OSError:
            print('Exception')
            break

def main():
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=2991)
    loop.run_until_complete(f)
    try:
        loop.run_forever()
    finally:
        loop.stop()
        print('here')

if __name__ == '__main__':
    main()
