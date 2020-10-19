import socket
import sys

#set up to send file
s = socket.socket()
s.connect(("localhost",9999))
f = open ("happy.txt", "rb")
l = f.read(1024)
while (l):
        s.send(l)
        l = f.read(1024)
s.close()
