'''
  Simple socket server using threads.
'''

import socket
import sys
from _thread import start_new_thread
from car import Car

HOST = '' # Symbolic name meaning all available interfaces.
PORT = 5555 # Arbitrary non-privileged port.

class Server:

  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    self.car = Car()
    self.car.start()

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

    # Start printing out the car status.
    print('Car engine is ON')
    self.car.attach_observer()

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
    # Infinite loop that will finish on client disconnect.
    while True:
      # Receiving from client.
      data = conn.recv(1024)
      if not data:
        break

      tokens = data.split()
      if data == b'\n':
        reply = ''
      elif len(tokens) == 1 and tokens[0] == b'STATUS':
        reply = self.car.status() + '\n'
      elif len(tokens) == 2 and tokens[0] == b'THROTTLE' and self.is_percentage(tokens[1]):
        self.car.set_throttle_percentage(float(tokens[1]))
        reply = 'OK\n'
      else:
        reply = 'Command malformed - ignored\n'

      conn.sendall(reply.encode('utf-8'))
  
    # Came out of loop.
    conn.close()

  def is_percentage(self, bstr):
    if not bstr.decode('utf-8').replace('.','',1).isdigit():
      return False
    percentage = float(bstr.decode('utf-8'))
    return percentage >= 0 and percentage <= 100

  def close(self):
    self.socket.close()

if __name__ == '__main__':
  server = Server()
  server.bind()
  server.listen()
