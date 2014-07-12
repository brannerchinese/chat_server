# behnke_server.py
# Based on https://gist.github.com/dbehnke/9627160
# 20140711

"""Launch AsyncIO Server"""

import asyncio

clients = {}           # task:  (reader, writer)
clients_by_login = {}  # login: (reader, writer)

def accept_client(client_reader, client_writer):
    """Accept client and delete when finished."""
    task = asyncio.Task(handle_client(client_reader, client_writer))
    clients[task] = (client_reader, client_writer)
    def client_done(task):
        """Delete client."""
        del clients[task]
        client_writer.close()
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
def handle_client(client_reader, client_writer):
    # Begin client log-in: 
    #   establish connection and add login to clients_by_login.
    login = ''
    while not login:
        client_writer.write("Connection made.\n".encode())
        data = yield from asyncio.wait_for(
                client_reader.readline(), timeout=None)
        if data is None:
            continue
        login = data.decode().rstrip()
        print('Received {}'.format(login))
        # Store log-in: client in dictionary QQQ
        clients_by_login[login] = (client_reader, client_writer)
        print('all clients_by_login:', clients_by_login)
    # now be an echo back server until client sends a bye
    i = 0  # sequence number
    # let client know we are ready
    client_writer.write("ready for messages\n".encode())
    while True:
        i = i + 1
        # wait for input from client
        data = yield from asyncio.wait_for(
                client_reader.readline(), timeout=None)
        if data is None:
            print("Received no data")
            # exit echo loop and disconnect
            return

        sdata = data.decode().rstrip()
        if sdata.lower() == 'bye':
            client_writer.write("BYE\n".encode())
            break
        response = ("ECHO {}: {}\n".format(i, sdata))
        try:
            client_writer.write(response.encode())
        except OSError:
            print('Exception')
            break

def main():
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(accept_client, host=None, port=2991)
    loop.run_until_complete(f)
    loop.run_forever()

if __name__ == '__main__':
    main()
