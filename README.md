## Chat Server

Build a chat server and client to work with it. 

Original [Iron Forger](https://hackpad.com/Iron-Forger-kEmauANGcV5) assignment is at https://hackpad.com/Week-6-Chat-Server-Client-rIxE6ZfW1sN.

### Currently working

`server.py`, `client.py`

 * Using Python 3.4's `asyncio` module and `asyncio.streams.StreamReader` and `asyncio.streams.StreamWriter` objects. 
 * Multiple clients can log into the same server.
 * Each client logs in with its own log-in, and a dictionary is populated, `login: (StreamReader, StreamWrite)`.
 * The server and each client choose the port over which they communicate at random. The same seed must be supplied:

        python server.py oh_a_seed_here
        python client.py oh_a_seed_here

   etc. If no seed is supplied, the programs use a default seed. If the seeds used are not the same, then the client will not be able to contact the server.

### Currently not working

 * Although each client can communicate independently with the single server, they cannot communicate with each other. An effort is made in `server2.py`, `client2.py` to allow different clients to communicate by way of the server, but it is not working now.

### Next

 * Implement message functionality.
 * Handle commands from the client to the server:
   * `?h`: list of commands
   * `?u`: list of logged-in users
   * `q`: quit
   * `>u[, u2, ...]: message`: send `message` to user(s) `u`, `u2`, etc. 

[end]
