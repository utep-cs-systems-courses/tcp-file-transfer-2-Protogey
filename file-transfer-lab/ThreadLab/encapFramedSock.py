import re, sys
import os.path
from os import path

class EncapFramedSock:               # a facade
  def __init__(self, sockAddr):
    self.sock, self.addr = sockAddr
    self.rbuf = b""         # receive buffer

  def close(self):
    return self.sock.close()

  def sendName(self, name, debugPrint=0):
    self.sock.send(name.encode())
    print("Sent Name")

  def receiveName(self, debugPrint=0):
    name = self.sock.recv(1024)
    print("received file name")
    return name.decode()

  #updated to take in name instead of payload
  def send(self, name, debugPrint=0):
    name = name.strip()#strip of spaces
    print("Sending: ", name)
    #if the file does not exist in the directory, exit
    if not path.exists(name):
      print("file does not exists!")
      sys.exit(1)

    #open the file as readbytes, variable f
    with open(name, 'rb') as f:
      #read 1024 bytes from the file.
      l = f.read(1024)
      print("text: ", l.decode())
      #read until end, and send after every read
      while(l):
        self.sock.send(l)
        l = f.read(1024)
      print("Sent..!")

  #updated to receive a file and "received file"
  def receive(self, name, debugPrint=0):
    name = name.strip()#strip spaces
    print("Receiving..!")
    with open(name, 'wb') as f:
      data = self.sock.recv(1024)#received data
      print("text: ", data.decode())
      while (data):#write given data, continue to read
        #i had a hanging recv in this part, just skipped.
        f.write(data)
        data = ''#self.sock.recv(1024)
      print("Received..!")
