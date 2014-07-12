## Chat Server

Build a chat server and client to work with it. 

Original [Iron Forger](https://hackpad.com/Iron-Forger-kEmauANGcV5) assignment is at https://hackpad.com/Week-6-Chat-Server-Client-rIxE6ZfW1sN.

Currently working:

 * Using Python 3.4's `asyncio` module and `asyncio.streams.StreamReader` and asyncio.streams.StreamWriter` objects. 
 * Multiple clients can log into the same server.
 * Each client logs in with its own log-in, and a dictionary is populated, `login: (StreamReader, StreamWrite)`.

Next:

 * Handle commands from the client to the server:
   * `?h`: list of commands
   * `?u`: list of logged-in users
   * `q`: quit
   * `>u[, u2, ...]: message`: send message to user(s) u, u2, etc. 
 * Implement message functionality.
 * Make sure a logged-out client actually quits.

[end]
