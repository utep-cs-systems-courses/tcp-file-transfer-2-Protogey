import re
import os.path
from os import path

class EncapFramedSock:               # a facade
  def __init__(self, sockAddr):
    self.sock, self.addr = sockAddr
    self.rbuf = b""         # receive buffer

  def close(self):
    return self.sock.close()

  def send(self, name, debugPrint=0):
    name = name.strip()
    print("Sending: ", name)
    if not path.exists(name):
      print("file does not exists!")
      sys.exit(1)
      
    #self.sock.send(name.encode())
    with open(name, 'rb') as f:
      l = f.read(1024)
      print("text: ", l.decode())
      while(l):
        self.sock.send(l)
        l = f.read(1024)
      print("Sent..!")
      
  def receive(self, debugPrint=0):
    #name = name.strip()
    print("Receiving..!")
    with open("Received_file", 'wb') as f:
      data = self.sock.recv(1024)
      print("text: ", data.decode())
      while (data):
        f.write(data)
        data = ''#self.sock.recv(1024)
      print("Received..!")
