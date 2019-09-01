'''
  Simple socket server using threads.
'''

import socket
import sys
from _thread import start_new_thread

HOST = '' # Symbolic name meaning all available interfaces.
PORT = 5555 # Arbitrary non-privileged port.

class Server:

  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

  def bind(self):
    # BIND socket to local host and port.
    try:
      self.socket.bind((HOST, PORT))
    except socket.error as msg:
      print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
      sys.exit()      
    print('Socket bind complete')

  def listen(self):
    # Start listening on socket.
    self.socket.listen(10)
    print('Socket now listening')

    # Now keep talking with the client.
    while True:
        # Wait to accept a connection - blocking call.
      conn, addr = self.socket.accept()
      print('Connected with ' + addr[0] + ':' + str(addr[1]))
      
      # Start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function..
      start_new_thread(self._clientthread , (conn,))

  # Function for handling connections. This will be used to create threads.
  def _clientthread(self, conn):
    # Sending message to connected client.
    conn.send(b'Welcome to the server. Type something and hit enter\n')
    
    # Infinite loop so that function do not terminate and thread do not end..
    while True:
      # Receiving from client.
      data = conn.recv(1024)
      if not data:
        break
      reply = b'OK...' + data
      conn.sendall(reply)
  
    # Came out of loop.
    conn.close()

  def close(self):
    self.socket.close()

if __name__ == '__main__':
  server = Server()
  server.bind()
  server.listen()
