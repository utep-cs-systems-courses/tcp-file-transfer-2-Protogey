import socket
import sys

s = socket.socket()
s.bind(("localhost",9999))
s.listen(10) # listen upto 10 connections, no fork yet. this is file transfer
while True:
    sc, address = s.accept()
    i=1
    f = open('file_'+ str(i)+".txt",'wb') #open
    i=i+1


    while (True):
        # receive data and write it to file
        l = sc.recv(1024)
        while (l):
            f.write(l)
            l = sc.recv(1024)
    f.close()
    sc.close()
s.close()
